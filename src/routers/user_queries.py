import time
import uuid
from typing import Any

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from src.response_api.text_generation.v2 import GeneratorV2
from src.models.corrections import CorrectionsRepository
from src.models.search_event import SearchEventRepository

user_queries_router = APIRouter()

SUPPORTED_API_VERSION = "v1"


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


@user_queries_router.get('/', tags=['User Queries'])
@user_queries_router.get('/v1', tags=['User Queries'])
def get_response(
    user_query: str,
    platform: str = "magento",
    tenant_id: str = "default",
    locale: str = "es_AR",
    store_code: str = "default",
    session_id: str | None = None,
):
    request_id = str(uuid.uuid4())
    started_at = time.time()
    source = "ia"
    fallback_reason = None

    try:
        consult_class = GeneratorV2()
        raw_content = consult_class.extract_search_intent(user_query=user_query)
        response_payload = _normalize_response_block(
            raw_content.get('response', {}) if isinstance(raw_content, dict) else {}
        )
        attributes = response_payload.get('characteristics', [])

        raw_filters = consult_class.get_embedding_filter_by_attributes(
            attributes=attributes,
            platform=platform,
            tenant_id=tenant_id,
            locale=locale,
            store_code=store_code,
            min_similarity=0.30,
            top_k=2
        )
        filters = _normalize_filters(raw_filters)

        corrections_repo = CorrectionsRepository()
        filters, applied_corrections = corrections_repo.apply_corrections(
            filters=filters,
            query_text=user_query,
            platform=platform,
            tenant_id=tenant_id,
            locale=locale,
        )

        if not filters:
            source = "fallback"
            fallback_reason = "empty_embedding_matches"

        content = {
            "response": response_payload,
            "input_tokens": _to_int(raw_content.get("input_tokens", 0) if isinstance(raw_content, dict) else 0),
            "output_tokens": _to_int(raw_content.get("output_tokens", 0) if isinstance(raw_content, dict) else 0),
            "total_tokens": _to_int(raw_content.get("total_tokens", 0) if isinstance(raw_content, dict) else 0),
            "filters": filters,
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
            "filters": []
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

    ia_response = JSONResponse(content=jsonable_encoder(content))
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
