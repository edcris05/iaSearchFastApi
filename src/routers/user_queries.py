import json
import logging
import os
import time
import uuid
from typing import Any

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from src.models.contracts import SearchResponseOut
from src.response_api.text_generation.v2 import GeneratorV2
from src.models.corrections import CorrectionsRepository
from src.models.query_rules import QueryRulesResolver
from src.models.search_event import SearchEventRepository
from src.utils.domain_profile import resolve_domain_profile, resolve_numeric_aliases
from src.utils.intent_normalization import normalize_response_block
from src.utils.scope_config import (
    DEFAULT_LOCALE,
    DEFAULT_PLATFORM,
    DEFAULT_STORE_CODE,
    DEFAULT_TENANT_ID,
)

user_queries_router = APIRouter()
logger = logging.getLogger(__name__)

SUPPORTED_API_VERSION = "v1"
# Baseline global defaults should remain provider-agnostic.
# Project/tenant-specific attribute codes must be configured via env var
# EMBEDDING_MIN_SIMILARITY_BY_ATTRIBUTE in each deployment.
DEFAULT_ATTRIBUTE_MIN_SIMILARITY: dict[str, float] = {}


def _to_number_or_none(value: Any):
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return value
    try:
        if "." in str(value):
            return float(value)
        return int(value)
    except Exception:
        return None


def _normalize_filters(filters: Any) -> list:
    if not isinstance(filters, list):
        return []

    normalized = []
    for group in filters:
        if not isinstance(group, list):
            continue

        group_out = []
        for candidate in group:
            if not isinstance(candidate, list) or len(candidate) < 5:
                continue

            field = str(candidate[0]).strip()
            if field == "":
                continue

            value_string = "" if candidate[1] is None else str(candidate[1]).strip()
            value_number = _to_number_or_none(candidate[2])
            phrase = "" if candidate[3] is None else str(candidate[3]).strip()
            similarity = _to_number_or_none(candidate[4])
            similarity = 0.0 if similarity is None else float(similarity)

            group_out.append([
                field,
                value_string,
                value_number,
                phrase,
                similarity,
            ])

        if group_out:
            normalized.append(group_out)

    return normalized


def _to_int(value: Any) -> int:
    try:
        return int(value)
    except Exception:
        return 0


def _empty_retrieval(top_k: int, min_similarity: float) -> dict:
    return {
        "strategy": "top_k_per_attribute",
        "top_k": max(1, min(5, int(top_k))),
        "min_similarity": float(min_similarity),
        "attributes": [],
    }


def _flatten_filters(filters: list) -> list[list[Any]]:
    flat: list[list[Any]] = []
    for group in filters:
        if not isinstance(group, list):
            continue
        for item in group:
            if isinstance(item, list) and len(item) >= 5:
                flat.append(item)
    return flat


def _group_filters_by_attribute(flat_filters: list[list[Any]]) -> list:
    by_attr: dict[str, list[list[Any]]] = {}
    for item in flat_filters:
        attr = str(item[0]).strip()
        if attr == "":
            continue
        by_attr.setdefault(attr, []).append(item)

    grouped: list = []
    for _, items in by_attr.items():
        grouped.append(items)
    return grouped


def _load_attribute_min_similarity(global_min_similarity: float) -> dict[str, float]:
    thresholds = {
        key: float(max(0.0, min(1.0, value)))
        for key, value in DEFAULT_ATTRIBUTE_MIN_SIMILARITY.items()
    }

    def enforce_global_min(values: dict[str, float]) -> dict[str, float]:
        # Allow per-attribute overrides to be lower than the request/global min.
        # This is needed to keep strict globals (e.g. 0.90) while relaxing only
        # noisy/specific attributes explicitly configured in env.
        return values

    raw = os.getenv("EMBEDDING_MIN_SIMILARITY_BY_ATTRIBUTE", "").strip()
    if raw == "":
        return enforce_global_min(thresholds)

    try:
        parsed = json.loads(raw)
    except Exception:
        return enforce_global_min(thresholds)

    if not isinstance(parsed, dict):
        return enforce_global_min(thresholds)

    for key, value in parsed.items():
        attr = str(key).strip()
        if attr == "":
            continue
        try:
            numeric = float(value)
        except Exception:
            continue
        thresholds[attr] = max(0.0, min(1.0, numeric))

    # Nunca usar un umbral por atributo menor al umbral global.
    return enforce_global_min(thresholds)


@user_queries_router.get('/', tags=['User Queries'])
@user_queries_router.get('/v1', tags=['User Queries'])
def get_response(
    user_query: str,
    platform: str = DEFAULT_PLATFORM,
    tenant_id: str = DEFAULT_TENANT_ID,
    locale: str = DEFAULT_LOCALE,
    store_code: str = DEFAULT_STORE_CODE,
    session_id: str | None = None,
    min_similarity: float = 0.30,
    top_k: int = 3,
) -> SearchResponseOut:
    request_id = str(uuid.uuid4())
    started_at = time.time()
    source = "ia"
    fallback_reason = None
    redirect_url = None
    redirect_match = None

    top_k = max(1, min(5, int(top_k)))
    if min_similarity < 0.0 or min_similarity > 1.0:
        min_similarity = 0.30
    attribute_min_similarity = _load_attribute_min_similarity(min_similarity)
    domain_profile = resolve_domain_profile(
        platform=platform,
        tenant_id=tenant_id,
        locale=locale,
        store_code=store_code,
    )
    numeric_aliases = resolve_numeric_aliases(
        platform=platform,
        tenant_id=tenant_id,
        locale=locale,
        store_code=store_code,
    )

    query_rules = QueryRulesResolver()
    query_rules_result = query_rules.resolve(
        query=user_query,
        platform=platform,
        tenant_id=tenant_id,
        locale=locale,
        store_code=store_code,
    )
    query_after_stopwords = str(query_rules_result.get("query_after_stopwords", user_query)).strip() or user_query
    removed_stopwords = query_rules_result.get("removed_stopwords", [])
    if not isinstance(removed_stopwords, list):
        removed_stopwords = []
    removed_stopwords = [str(item).strip() for item in removed_stopwords if str(item).strip() != ""]

    redirect_info = query_rules_result.get("redirect_match")
    if isinstance(redirect_info, dict):
        redirect_url = str(redirect_info.get("url", "")).strip() or None
        redirect_match = str(redirect_info.get("matched_phrase", "")).strip() or None

    if redirect_url:
        source = "redirect"
        fallback_reason = "redirect_rule_match"
        content = {
            "response": {
                "price_min": None,
                "price_max": None,
                "min_battery_mah": None,
                "min_ram_gb": None,
                "min_storage_gb": None,
                "characteristics": []
            },
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
            "filters": [],
            "retrieval": _empty_retrieval(top_k=top_k, min_similarity=min_similarity),
            "applied_corrections": [],
        }
    else:
        try:
            consult_class = GeneratorV2()
            raw_content = consult_class.extract_search_intent(
                user_query=query_after_stopwords,
                platform=platform,
                tenant_id=tenant_id,
                locale=locale,
                store_code=store_code,
            )
            response_payload = normalize_response_block(
                raw_content.get('response', {}) if isinstance(raw_content, dict) else {},
                numeric_aliases=numeric_aliases,
            )
            attributes = response_payload.get('characteristics', [])

            retrieval_payload = consult_class.get_embedding_filter_by_attributes(
                attributes=attributes,
                query_text=query_after_stopwords,
                platform=platform,
                tenant_id=tenant_id,
                locale=locale,
                store_code=store_code,
                min_similarity=min_similarity,
                top_k=top_k,
                attribute_min_similarity=attribute_min_similarity,
            )
            if isinstance(retrieval_payload, dict):
                raw_filters = retrieval_payload.get("selected_filters", [])
                retrieval = retrieval_payload.get("retrieval", _empty_retrieval(top_k=top_k, min_similarity=min_similarity))
            else:
                raw_filters = retrieval_payload
                retrieval = _empty_retrieval(top_k=top_k, min_similarity=min_similarity)

            filters = _normalize_filters(raw_filters)

            # Fallback semántico multi-tenant/multi-plataforma:
            # si embeddings no devuelve matches pero hay characteristics,
            # hacemos una segunda recuperación con la query completa para
            # rescatar atributos compuestos (ej: color + manufacturer).
            if not filters and attributes:
                fallback_retrieval_payload = consult_class.get_embedding_filter_by_attributes(
                    attributes=[query_after_stopwords],
                    query_text=query_after_stopwords,
                    platform=platform,
                    tenant_id=tenant_id,
                    locale=locale,
                    store_code=store_code,
                    min_similarity=min_similarity,
                    top_k=top_k,
                    attribute_min_similarity=attribute_min_similarity,
                )

                if isinstance(fallback_retrieval_payload, dict):
                    fallback_raw_filters = fallback_retrieval_payload.get("selected_filters", [])
                    fallback_filters = _normalize_filters(fallback_raw_filters)
                    if fallback_filters:
                        merged_flat = _flatten_filters(filters) + _flatten_filters(fallback_filters)
                        filters = _group_filters_by_attribute(merged_flat)
                        retrieval = fallback_retrieval_payload.get("retrieval", retrieval)

            corrections_repo = CorrectionsRepository()
            filters, applied_corrections = corrections_repo.apply_corrections(
                filters=filters,
                query_text=query_after_stopwords,
                platform=platform,
                tenant_id=tenant_id,
                locale=locale,
            )

            has_structured_intent = any([
                response_payload.get("price_min") is not None,
                response_payload.get("price_max") is not None,
                response_payload.get("min_battery_mah") is not None,
                response_payload.get("min_ram_gb") is not None,
                response_payload.get("min_storage_gb") is not None,
            ])

            if filters:
                source = "semantic"
            elif has_structured_intent:
                # IA extrajo intención estructurada válida (ej. price_max) aunque
                # embeddings no haya aportado filtros adicionales.
                source = "ia"
                fallback_reason = None
            elif attributes:
                source = "fallback"
                fallback_reason = "empty_embedding_matches"
            else:
                source = "ia"
                fallback_reason = None

            content = {
                "response": response_payload,
                "input_tokens": _to_int(raw_content.get("input_tokens", 0) if isinstance(raw_content, dict) else 0),
                "output_tokens": _to_int(raw_content.get("output_tokens", 0) if isinstance(raw_content, dict) else 0),
                "total_tokens": _to_int(raw_content.get("total_tokens", 0) if isinstance(raw_content, dict) else 0),
                "filters": filters,
                "retrieval": retrieval,
                "applied_corrections": applied_corrections,
            }
        except Exception:
            logger.exception("query processing failed request_id=%s", request_id)
            source = "fallback"
            fallback_reason = "query_processing_error"
            content = {
                "response": {
                    "price_min": None,
                    "price_max": None,
                    "min_battery_mah": None,
                    "min_ram_gb": None,
                    "min_storage_gb": None,
                    "characteristics": []
                },
                "input_tokens": 0,
                "output_tokens": 0,
                "total_tokens": 0,
                "filters": [],
                "retrieval": _empty_retrieval(top_k=top_k, min_similarity=min_similarity),
                "applied_corrections": [],
            }

    latency_ms = int((time.time() - started_at) * 1000)
    content["meta"] = {
        "api_version": SUPPORTED_API_VERSION,
        "request_id": request_id,
        "source": source,
        "fallback_reason": fallback_reason,
        "redirect_url": redirect_url,
        "redirect_match": redirect_match,
        "latency_ms": latency_ms,
        "platform": platform,
        "tenant_id": tenant_id,
        "locale": locale,
        "store_code": store_code,
        "query_after_stopwords": query_after_stopwords,
        "removed_stopwords": removed_stopwords,
        "domain_profile": domain_profile,
    }

    try:
        metrics_repo = SearchEventRepository()
        metrics_repo.log_event(
            {
                "request_id": request_id,
                "platform": platform,
                "tenant_id": tenant_id,
                "session_id": session_id,
                "event_type": "search",
                "query_text": user_query,
                "source": source,
                "fallback_reason": fallback_reason,
                "api_version": SUPPORTED_API_VERSION,
                "latency_ms": latency_ms,
                "filters": content.get("filters", []),
                "product_id": None,
                "position": None,
            }
        )
    except Exception:
        pass

    response_payload = SearchResponseOut.model_validate(content)
    ia_response = JSONResponse(content=jsonable_encoder(response_payload.model_dump()))
    return ia_response

# # With v1
# {
#   "response": {
#     "query": "celular con buena batería",
#     "price_min": null,
#     "price_max": null,
#     "attributes": [
#       "buena batería"
#     ]
#   },
#   "input_tokens": 251,
#   "output_tokens": 41,
#   "total_tokens": 292
# }


# # With v2
# {
#   "response": {
#     "price_min": null,
#     "price_max": null,
#     "min_battery_mah": null,
#     "attributes": [
#       "celular con buena batería"
#     ]
#   },
#   "input_tokens": 164,
#   "output_tokens": 46,
#   "total_tokens": 210
# }
