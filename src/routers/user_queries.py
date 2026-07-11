import json
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
from src.models.search_event import SearchEventRepository

user_queries_router = APIRouter()

SUPPORTED_API_VERSION = "v1"
# Baseline global defaults should remain provider-agnostic.
# Project/tenant-specific attribute codes must be configured via env var
# EMBEDDING_MIN_SIMILARITY_BY_ATTRIBUTE in each deployment.
DEFAULT_ATTRIBUTE_MIN_SIMILARITY = {
    "color": 0.45,
}


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


def _normalize_response_block(response_payload: Any) -> dict:
    payload = response_payload if isinstance(response_payload, dict) else {}
    characteristics = payload.get("characteristics", [])
    if not isinstance(characteristics, list):
        characteristics = []

    return {
        "price_min": _to_number_or_none(payload.get("price_min")),
        "price_max": _to_number_or_none(payload.get("price_max")),
        "min_battery_mah": _to_number_or_none(payload.get("min_battery_mah")),
        "min_ram_gb": _to_number_or_none(payload.get("min_ram_gb")),
        "min_storage_gb": _to_number_or_none(payload.get("min_storage_gb")),
        "characteristics": [str(c).strip() for c in characteristics if str(c).strip() != ""],
    }


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


def _load_attribute_min_similarity(global_min_similarity: float) -> dict[str, float]:
    thresholds = {
        key: float(max(0.0, min(1.0, value)))
        for key, value in DEFAULT_ATTRIBUTE_MIN_SIMILARITY.items()
    }

    raw = os.getenv("EMBEDDING_MIN_SIMILARITY_BY_ATTRIBUTE", "").strip()
    if raw == "":
        return thresholds

    try:
        parsed = json.loads(raw)
    except Exception:
        return thresholds

    if not isinstance(parsed, dict):
        return thresholds

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
    for key, value in list(thresholds.items()):
        if value < global_min_similarity:
            thresholds[key] = global_min_similarity

    return thresholds


@user_queries_router.get('/', tags=['User Queries'])
@user_queries_router.get('/v1', tags=['User Queries'])
def get_response(
    user_query: str,
    platform: str = "magento",
    tenant_id: str = "default",
    locale: str = "es_AR",
    store_code: str = "default",
    session_id: str | None = None,
    min_similarity: float = 0.30,
    top_k: int = 3,
) -> SearchResponseOut:
    request_id = str(uuid.uuid4())
    started_at = time.time()
    source = "ia"
    fallback_reason = None

    top_k = max(1, min(5, int(top_k)))
    if min_similarity < 0.0 or min_similarity > 1.0:
        min_similarity = 0.30
    attribute_min_similarity = _load_attribute_min_similarity(min_similarity)

    try:
        consult_class = GeneratorV2()
        raw_content = consult_class.extract_search_intent(user_query=user_query)
        response_payload = _normalize_response_block(
            raw_content.get('response', {}) if isinstance(raw_content, dict) else {}
        )
        attributes = response_payload.get('characteristics', [])

        retrieval_payload = consult_class.get_embedding_filter_by_attributes(
            attributes=attributes,
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

        corrections_repo = CorrectionsRepository()
        filters, applied_corrections = corrections_repo.apply_corrections(
            filters=filters,
            query_text=user_query,
            platform=platform,
            tenant_id=tenant_id,
            locale=locale,
        )

        if filters:
            source = "semantic"
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
        "latency_ms": latency_ms,
        "platform": platform,
        "tenant_id": tenant_id,
        "locale": locale,
        "store_code": store_code,
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
