import re
from typing import Any

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.models.chat_session_context import ChatSessionContextRepository
from src.models.contracts import ChatTurnIn, ChatTurnOut
from src.response_api.text_generation.v2 import GeneratorV2

chat_turn_router = APIRouter()


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


def _normalize_filters(filters: Any) -> list[list[list[Any]]]:
    if not isinstance(filters, list):
        return []

    normalized: list[list[list[Any]]] = []
    for group in filters:
        if not isinstance(group, list):
            continue

        group_out: list[list[Any]] = []
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


def _flatten_filters(filters: list[list[list[Any]]]) -> list[list[Any]]:
    flat: list[list[Any]] = []
    for group in filters:
        for item in group:
            if isinstance(item, list) and len(item) >= 5:
                flat.append(item)
    return flat


def _group_flat_filters(flat_filters: list[list[Any]]) -> list[list[list[Any]]]:
    out: list[list[list[Any]]] = []
    for item in flat_filters:
        out.append([item])
    return out


def _detect_operation(message: str, explicit_operation: str | None) -> str:
    if explicit_operation in ("add", "replace", "remove", "reset"):
        return explicit_operation

    msg = message.strip().lower()
    if msg == "":
        return "add"

    if any(token in msg for token in ["reiniciar", "reset", "empezar de nuevo", "limpiar todo"]):
        return "reset"

    if any(token in msg for token in ["saca", "sacar", "quita", "quitar", "remove", "sin "]):
        return "remove"

    if any(token in msg for token in ["solo ", "solamente", "cambiar", "cambia", "en lugar de"]):
        return "replace"

    return "add"


def _merge_filters(
    previous_filters: list[list[list[Any]]],
    incoming_filters: list[list[list[Any]]],
    operation: str,
) -> list[list[list[Any]]]:
    prev_flat = _flatten_filters(previous_filters)
    in_flat = _flatten_filters(incoming_filters)

    if operation == "reset":
        return _group_flat_filters(in_flat)

    if operation == "remove":
        if not in_flat:
            return previous_filters

        remove_fields = {str(item[0]).strip() for item in in_flat if str(item[0]).strip() != ""}
        kept = [item for item in prev_flat if str(item[0]).strip() not in remove_fields]
        return _group_flat_filters(kept)

    # add / replace
    by_field: dict[str, list[list[Any]]] = {}
    for item in prev_flat:
        field = str(item[0]).strip()
        if field == "":
            continue
        by_field.setdefault(field, []).append(item)

    for item in in_flat:
        field = str(item[0]).strip()
        if field == "":
            continue

        if operation == "replace":
            by_field[field] = [item]
            continue

        # add: append unique values for same field
        existing = by_field.get(field, [])
        sig = (str(item[1]), str(item[2]), str(item[3]))
        exists = False
        for current in existing:
            current_sig = (str(current[1]), str(current[2]), str(current[3]))
            if current_sig == sig:
                exists = True
                if float(item[4]) > float(current[4]):
                    current[4] = float(item[4])
                break

        if not exists:
            existing.append(item)
            by_field[field] = existing

    merged_flat: list[list[Any]] = []
    for _, items in by_field.items():
        for item in items:
            merged_flat.append(item)

    # keep highest confidence entries first for deterministic output
    merged_flat.sort(key=lambda x: float(x[4]) if len(x) > 4 else 0.0, reverse=True)

    return _group_flat_filters(merged_flat)


def _detect_intent(message: str, merged_filters: list[list[list[Any]]], operation: str) -> str:
    if operation == "reset":
        return "reset_context"
    if operation == "remove":
        return "remove_filters"

    msg = message.strip().lower()
    if "carrito" in msg:
        return "cart_related"

    if _flatten_filters(merged_filters):
        return "refine_search"

    return "open_question"


def _filters_to_human_text(filters: list[list[list[Any]]]) -> str:
    parts: list[str] = []
    for item in _flatten_filters(filters):
        field = str(item[0]).strip()
        value_string = str(item[1]).strip()
        value_number = item[2]

        if value_number is not None and str(value_number) != "":
            value_text = str(value_number)
        else:
            value_text = value_string

        if value_text == "":
            continue

        if field == "manufacturer":
            parts.append(f"marca {value_text}")
        elif field == "price":
            parts.append(f"precio {value_text}")
        elif field == "color":
            parts.append(f"color {value_text}")
        else:
            parts.append(f"{field} {value_text}")

    return ", ".join(parts)


def _normalize_search_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text


def _build_search_text(previous_search_text: str, message: str, operation: str) -> str:
    message = _normalize_search_text(message)
    previous_search_text = _normalize_search_text(previous_search_text)

    if operation == "reset":
        return message

    if previous_search_text == "":
        return message

    if operation in ("add", "replace", "remove"):
        return _normalize_search_text(previous_search_text + " " + message)

    return message


def _build_explanation(operation: str, merged_filters: list[list[list[Any]]], detected_intent: str) -> str:
    summary = _filters_to_human_text(merged_filters)

    if operation == "reset":
        if summary:
            return f"Perfecto, reinicié la conversación y ahora busco por: {summary}."
        return "Listo, reinicié la conversación. Contame qué querés buscar ahora."

    if operation == "remove":
        if summary:
            return f"Hecho, quité ese criterio y ahora quedaron activos: {summary}."
        return "Hecho, quité esos criterios. Decime qué querés agregar ahora."

    if detected_intent == "open_question":
        return "Entendido. Contame más detalles del producto y voy refinando la búsqueda con vos."

    if summary:
        return f"Perfecto, actualicé tu búsqueda. Filtros activos: {summary}."

    return "Perfecto, actualicé la búsqueda."


@chat_turn_router.post("/", tags=["Chat"])
def chat_turn(payload: ChatTurnIn):
    operation = _detect_operation(payload.message, payload.operation)

    repo = ChatSessionContextRepository()
    repo.ensure_table()

    previous = repo.load_context(
        platform=payload.platform,
        tenant_id=payload.tenant_id,
        locale=payload.locale,
        store_code=payload.store_code,
        chat_session_id=payload.chat_session_id,
    ) or {
        "filters": [],
        "search_text": "",
    }

    previous_filters = _normalize_filters(previous.get("filters", []))

    incoming_filters: list[list[list[Any]]] = []
    if payload.message.strip() != "":
        try:
            generator = GeneratorV2()
            intent = generator.extract_search_intent(user_query=payload.message)
            response = intent.get("response", {}) if isinstance(intent, dict) else {}
            attrs = response.get("characteristics", []) if isinstance(response, dict) else []
            retrieval_payload = generator.get_embedding_filter_by_attributes(
                attributes=attrs,
                query_text=payload.message,
                platform=payload.platform,
                tenant_id=payload.tenant_id,
                locale=payload.locale,
                store_code=payload.store_code,
                min_similarity=payload.min_similarity,
                top_k=payload.top_k,
                attribute_min_similarity=None,
            )
            if isinstance(retrieval_payload, dict):
                incoming_filters = _normalize_filters(retrieval_payload.get("selected_filters", []))
        except Exception:
            incoming_filters = []

    if operation == "reset" and payload.message.strip() == "":
        repo.reset_context(
            platform=payload.platform,
            tenant_id=payload.tenant_id,
            locale=payload.locale,
            store_code=payload.store_code,
            chat_session_id=payload.chat_session_id,
        )
        content = ChatTurnOut(
            chat_session_id=payload.chat_session_id,
            operation="reset",
            detected_intent="reset_context",
            explanation="Listo, limpié la conversación. Empecemos una búsqueda nueva.",
            context={
                "active_filters": [],
                "active_fields": [],
                "search_text": "",
            },
        )
        return JSONResponse(content=jsonable_encoder(content.model_dump()))

    merged_filters = _merge_filters(previous_filters, incoming_filters, operation)
    detected_intent = _detect_intent(payload.message, merged_filters, operation)

    search_text = _build_search_text(
        previous_search_text=str(previous.get("search_text", "")),
        message=payload.message,
        operation=operation,
    )

    explanation = _build_explanation(operation, merged_filters, detected_intent)

    new_context = {
        "filters": merged_filters,
        "search_text": search_text,
    }

    repo.save_context(
        platform=payload.platform,
        tenant_id=payload.tenant_id,
        locale=payload.locale,
        store_code=payload.store_code,
        chat_session_id=payload.chat_session_id,
        context=new_context,
    )

    active_fields = sorted(
        {
            str(item[0]).strip()
            for item in _flatten_filters(merged_filters)
            if str(item[0]).strip() != ""
        }
    )

    response_payload = ChatTurnOut(
        chat_session_id=payload.chat_session_id,
        operation=operation,
        detected_intent=detected_intent,
        explanation=explanation,
        context={
            "active_filters": merged_filters,
            "active_fields": active_fields,
            "search_text": search_text,
        },
    )

    return JSONResponse(content=jsonable_encoder(response_payload.model_dump()))
