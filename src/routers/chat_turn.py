import json
import logging
import re
from typing import Any

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.models.chat_session_context import ChatSessionContextRepository
from src.models.contracts import ChatTurnIn, ChatTurnOut
from src.response_api.text_generation.v2 import GeneratorV2

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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
    keep_segment = _extract_compound_keep_segment(message)
    if keep_segment != "":
        return "replace"

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


def _looks_like_new_search(message: str) -> bool:
    msg = message.strip().lower()
    if msg == "":
        return False

    additive_tokens = [
        "ademas",
        "además",
        "tambien",
        "también",
        "suma",
        "sumale",
        "agrega",
        "agregar",
        "agregá",
        "y tambien",
        "y también",
        "bien, ahora",
        "bien ahora",
        "ahora ",
        "quiero que",
    ]
    if any(token in msg for token in additive_tokens):
        return False

    words = re.findall(r"\w+", msg, flags=re.UNICODE)
    if len(words) >= 4:
        return True

    comparison_tokens = ["menor", "mayor", "hasta", "menos", "mas", "más", "entre", "desde", "precio"]
    if any(token in msg for token in comparison_tokens) and len(words) >= 3:
        return True

    return False


def _extract_compound_keep_segment(message: str) -> str:
    msg = _normalize_search_text(message)
    if msg == "":
        return ""

    msg_l = msg.lower()

    patterns = [
        r"(?:bien,?\s*)?(?:ahora,?\s*)?(?:tambi[eé]n\s+quiero\s+)?quita(?:r)?\s+todo(?:s)?\s+los?\s+filtros?\s+y\s+(?:busca(?:r)?|dej[aá]|dejame)\s+(.+)$",
        r"(?:bien,?\s*)?(?:ahora,?\s*)?(?:tambi[eé]n\s+quiero\s+)?quita(?:r)?\s+todo(?:s)?\s+los?\s+filtros?\s+pero\s+(?:dej[aá]|dejame|busca(?:r)?)\s+(.+)$",
        r"(?:bien,?\s*)?(?:ahora,?\s*)?(?:tambi[eé]n\s+quiero\s+)?saca(?:r)?\s+todo(?:s)?\s+los?\s+filtros?\s+y\s+(?:busca(?:r)?|dej[aá]|dejame)\s+(.+)$",
        r"(?:bien,?\s*)?(?:ahora,?\s*)?(?:tambi[eé]n\s+quiero\s+)?saca(?:r)?\s+todo(?:s)?\s+los?\s+filtros?\s+pero\s+(?:dej[aá]|dejame|busca(?:r)?)\s+(.+)$",
        r"(?:quita(?:r)?|saca(?:r)?)\s+todo(?:\s+lo)?\s+dem[aá]s\s+(?:y|pero)\s+(?:dej[aá]|dejame|deja)\s+(.+)$",
        r"(?:quita(?:r)?|saca(?:r)?)\s+todo(?:\s+lo)?\s+dem[aá]s\s+y\s+agreg[aá]\s+(.+)$",
        r"(?:quita(?:r)?|saca(?:r)?)\s+todo\s+menos\s+(.+)$",
        r"(?:quita(?:r)?|saca(?:r)?)\s+todo\s+excepto\s+(.+)$",
        r"(?:quita(?:r)?|saca(?:r)?)\s+todo\s+salvo\s+(.+)$",
        r"(?:deja(?:r)?|dej[aá]me)\s+solo\s+(.+)$",
        r"(?:deja(?:r)?|dej[aá]me)\s+únicamente\s+(.+)$",
        r"(?:deja(?:r)?|dej[aá]me)\s+solamente\s+(.+)$",
        r"(?:en\s+realidad\s+)?dej[aá]\s+solo\s+(.+)$",
    ]

    for pattern in patterns:
        m = re.search(pattern, msg_l, flags=re.IGNORECASE)
        if not m:
            continue
        keep = _normalize_search_text((m.group(1) or "").strip(" .,:;"))
        if keep != "":
            return keep

    return ""


def _is_compound_replace_after_remove(message: str, explicit_operation: str | None) -> bool:
    if explicit_operation in ("replace", "add"):
        return False

    msg = (message or "").strip().lower()
    if msg == "":
        return False

    has_remove = any(token in msg for token in [
        "quita",
        "quitar",
        "saca",
        "sacar",
        "remove",
    ])
    if not has_remove and "deja solo" not in msg and "todo menos" not in msg:
        return False

    keep_segment = _extract_compound_keep_segment(msg)
    return keep_segment != ""


def _merge_filters(
    previous_filters: list[list[list[Any]]],
    incoming_filters: list[list[list[Any]]],
    operation: str,
    message: str = "",
) -> list[list[list[Any]]]:
    prev_flat = _flatten_filters(previous_filters)
    in_flat = _flatten_filters(incoming_filters)

    if operation == "reset":
        return _group_flat_filters(in_flat)

    if operation == "remove":
        # En "remove" NO queremos depender de embeddings (incoming_filters) para saber qué sacar,
        # porque a veces embeddings devuelve otro color/nfc y no refleja la intención real del usuario.
        #
        # Estrategia:
        # - Si el texto del mensaje menciona explícitamente "color", eliminamos TODOS los filtros con field="color".
        # - Caso contrario, caemos al comportamiento previo: si incoming_filters trae fields, sacamos esos fields.
        msg_l = str(message or "").lower()

        # Mapeo de "conceptos" del usuario -> fields del catálogo
        # (acá solo se listan los que hoy importan; se puede extender)
        concept_to_fields: dict[str, set[str]] = {
            "color": {"color"},
            "marca": {"manufacturer"},
            "manufacturer": {"manufacturer"},
            "precio": {"price"},
        }

        explicit_remove_fields: set[str] = set()

        # Si el mensaje contiene verbo de remover + concepto, lo removemos aunque no haya embeddings.
        if re.search(r"\\b(saca|sacar|quita|quitar|sin|remove)\\b", msg_l):
            for concept, fields in concept_to_fields.items():
                if re.search(rf"\\b{re.escape(concept)}\\b", msg_l):
                    explicit_remove_fields.update(fields)

        if explicit_remove_fields:
            kept = [item for item in prev_flat if str(item[0]).strip() not in explicit_remove_fields]
            return _group_flat_filters(kept)

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
    def _humanize_field(field: str) -> str:
        return field.replace("_", " ").strip()

    # Deduplicar por (field, value_string, value_number) para evitar repetir "color: 133, color: 133"
    seen: set[tuple[str, str, str]] = set()
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

        key = (field, value_string, "" if value_number is None else str(value_number))
        if key in seen:
            continue
        seen.add(key)

        human_field = _humanize_field(field)
        parts.append(f"{human_field}: {value_text}")

    return ", ".join(parts)


def _normalize_search_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text


def _extract_explicit_addition_segment(message: str) -> str:
    msg = _normalize_search_text(message).lower()
    if msg == "":
        return ""

    patterns = [
        r"^(?:bien,?\s*)?(?:ahora,?\s*)?(?:tambien|también|ademas|además)\s+(.+)$",
        r"^(?:bien,?\s*)?(?:ahora,?\s*)?(?:y|e)\s+(.+)$",
        r"^(?:sumale|súmale|agrega|agregá|agregar)\s+(.+)$",
        r"^(?:bien,?\s*)?(?:ahora,?\s*)?quiero\s+que\s+(?:sea[n]?|me\s+muestres)\s+(.+)$",
        r"^(?:bien,?\s*)?(?:ahora,?\s*)?(?:que\s+)?sea[n]?\s+(.+)$",
    ]
    for pattern in patterns:
        m = re.search(pattern, msg, flags=re.IGNORECASE)
        if not m:
            continue
        seg = _normalize_search_text(m.group(1) or "")
        if seg != "":
            return seg

    return ""


def _strip_removed_tokens_from_search_text(previous_search_text: str, message: str) -> str:
    """
    Cuando el usuario pide 'quita X', debemos evitar que el search_text siga conteniendo X,
    porque eso vuelve a disparar embeddings/intent y reintroduce el filtro removido.
    """
    prev = _normalize_search_text(previous_search_text)
    msg = _normalize_search_text(message).lower()
    if prev == "" or msg == "":
        return prev

    wants_remove_color = bool(
        re.search(r"\\b(quita(?:r)?|saca(?:r)?)\\s+(?:el\\s+)?color\\b", msg)
    )

    if wants_remove_color:
        # soporta:
        # - "color negro" / "de color negro"
        # - "color: negro" / "de color: negro"
        # - token suelto "color"
        prev = re.sub(r"\\bde\\s+color\\s+[a-záéíóúñ0-9]+\\b", "", prev, flags=re.IGNORECASE)
        prev = re.sub(r"\\bcolor\\s*[=:]?\\s*[a-záéíóúñ0-9]+\\b", "", prev, flags=re.IGNORECASE)
        prev = re.sub(r"\\bcolor\\b", "", prev, flags=re.IGNORECASE)

    prev = re.sub(r"\\s+", " ", prev).strip()
    return prev


def _build_search_text(previous_search_text: str, message: str, operation: str) -> str:
    message = _normalize_search_text(message)
    previous_search_text = _normalize_search_text(previous_search_text)

    if operation == "reset":
        return message

    if operation == "replace":
        return message

    if operation == "remove":
        return _strip_removed_tokens_from_search_text(previous_search_text, message)

    if previous_search_text == "":
        return message

    if operation == "add":
        if message == "":
            return previous_search_text

        addition = _extract_explicit_addition_segment(message)
        if addition != "":
            if addition in previous_search_text:
                return previous_search_text
            return _normalize_search_text(previous_search_text + " " + addition)

        if message in previous_search_text:
            return previous_search_text
        if previous_search_text in message:
            return message
        return _normalize_search_text(previous_search_text + " " + message)

    return message


def _build_explanation(
    operation: str,
    merged_filters: list[list[list[Any]]],
    detected_intent: str,
    response_payload: dict[str, Any] | None = None,
    is_compound_replace_after_remove: bool = False,
) -> str:
    summary = _filters_to_human_text(merged_filters)
    response_payload = response_payload if isinstance(response_payload, dict) else {}

    def _format_money(value: Any) -> str:
        numeric = _to_number_or_none(value)
        if numeric is None:
            return ""
        try:
            return f"{int(float(numeric)):,}".replace(",", ".")
        except Exception:
            return str(numeric)

    price_min = response_payload.get("price_min")
    price_max = response_payload.get("price_max")
    min_battery = response_payload.get("min_battery_mah")
    min_ram = response_payload.get("min_ram_gb")
    min_storage = response_payload.get("min_storage_gb")

    intent_parts: list[str] = []
    if price_min is not None and price_max is not None:
        intent_parts.append(f"precio entre ${_format_money(price_min)} y ${_format_money(price_max)}")
    elif price_max is not None:
        intent_parts.append(f"precio hasta ${_format_money(price_max)}")
    elif price_min is not None:
        intent_parts.append(f"precio desde ${_format_money(price_min)}")

    if min_ram is not None:
        intent_parts.append(f"RAM desde {str(min_ram).strip()} GB")
    if min_storage is not None:
        intent_parts.append(f"almacenamiento desde {str(min_storage).strip()} GB")
    if min_battery is not None:
        intent_parts.append(f"batería desde {str(min_battery).strip()} mAh")

    intent_summary = ", ".join([p for p in intent_parts if p])

    if operation == "reset":
        if summary:
            return f"Perfecto, reinicié la conversación y ahora busco por: {summary}."
        if intent_summary:
            return f"Perfecto, reinicié la conversación y ahora busco por {intent_summary}."
        return "Listo, reinicié la conversación. Contame qué querés buscar ahora."

    if is_compound_replace_after_remove and summary:
        return f"Hecho, limpié los filtros anteriores y dejé solo: {summary}."

    if operation == "remove":
        if summary:
            return f"Hecho, quité ese criterio y ahora quedaron activos: {summary}."
        if intent_summary:
            return f"Hecho, quité ese criterio. Mantengo búsqueda por {intent_summary}."
        return "Hecho, quité esos criterios. Decime qué querés agregar ahora."

    if detected_intent == "open_question":
        return "Entendido. Contame más detalles del producto y voy refinando la búsqueda con vos."

    if summary and not intent_summary:
        return f"Perfecto, este es el resultado de tu búsqueda. Filtros activos: {summary}."

    if intent_summary:
        if summary:
            return (
                "Perfecto, este es el resultado de tu búsqueda. "
                f"Criterios detectados: {intent_summary}."
            )
        return f"Perfecto, este es el resultado de tu búsqueda. Criterios detectados: {intent_summary}."

    return "Perfecto, actualicé la búsqueda."


def _handle_chat_turn(payload: ChatTurnIn):
    operation = _detect_operation(payload.message, payload.operation)
    is_compound = _is_compound_replace_after_remove(payload.message, payload.operation)
    trace_id = f"{payload.chat_session_id}:{int(__import__('time').time() * 1000)}"
    logger.info("[chat_turn:%s] message=%r explicit_operation=%r detected_operation=%r", trace_id, payload.message, payload.operation, operation)

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
    logger.info(
        "[chat_turn:%s] previous search_text=%r prev_filters=%s",
        trace_id,
        str(previous.get("search_text", "")),
        json.dumps(_flatten_filters(previous_filters), ensure_ascii=False),
    )

    # Soporte para instrucciones compuestas en un único turno:
    # "quita todo ... y busca ...", "deja solo ...", "quita todo menos ...", etc.
    # Se interpreta como replace del nuevo criterio en el mismo mensaje.
    compound_keep_segment = ""
    if is_compound:
        compound_keep_segment = _extract_compound_keep_segment(payload.message)
        if compound_keep_segment != "":
            operation = "replace"

    # Si hay contexto previo y el mensaje parece una búsqueda nueva completa,
    # preferimos replace para evitar acumular filtros no intencionales.
    if operation == "add" and previous_filters and _looks_like_new_search(payload.message):
        logger.info("[chat_turn:%s] looks_like_new_search=True -> forcing replace", trace_id)
        operation = "replace"
    else:
        logger.info("[chat_turn:%s] looks_like_new_search=%s", trace_id, _looks_like_new_search(payload.message))

    incoming_filters: list[list[list[Any]]] = []
    response_payload: dict[str, Any] = {}
    message_for_intent = payload.message
    if compound_keep_segment != "":
        message_for_intent = compound_keep_segment

    # IMPORTANTE:
    # En operación "remove" NO debemos consultar intent/embeddings, porque:
    # - el usuario solo está pidiendo eliminar un filtro
    # - llamar embeddings agrega ruido (ej: NFC) y puede reintroducir atributos que se quieren quitar (color)
    if payload.message.strip() != "" and operation != "remove":
        try:
            generator = GeneratorV2()
            logger.info("[chat_turn:%s] message_for_intent=%r compound_keep_segment=%r", trace_id, message_for_intent, compound_keep_segment)
            intent = generator.extract_search_intent(
                user_query=message_for_intent,
                platform=payload.platform,
                tenant_id=payload.tenant_id,
                locale=payload.locale,
                store_code=payload.store_code,
            )
            response = intent.get("response", {}) if isinstance(intent, dict) else {}
            if isinstance(response, dict):
                response_payload = response
            attrs = response.get("characteristics", []) if isinstance(response, dict) else []
            logger.info(
                "[chat_turn:%s] intent.characteristics=%s response_payload=%s",
                trace_id,
                json.dumps(attrs, ensure_ascii=False),
                json.dumps(response_payload, ensure_ascii=False),
            )

            # Guardrail: si el intent trae "marca X", NO queremos que embeddings agregue colores random
            # o features accesorias (ej: NFC) que terminan sobre-restringiendo o contaminando la búsqueda.
            # En ese caso, restringimos por similarity más alto y top_k más bajo.
            msg_l = message_for_intent.lower()
            is_brand_phrase = bool(re.search(r"\\bmarca\\s+\\w+", msg_l, flags=re.IGNORECASE))
            if is_brand_phrase:
                pass1_min_sim = max(payload.min_similarity, 0.75)
                pass1_top_k = min(payload.top_k, 2)
            else:
                pass1_min_sim = payload.min_similarity
                pass1_top_k = payload.top_k

            logger.info(
                "[chat_turn:%s] retrieval pass1 attrs=%s min_similarity=%s top_k=%s is_brand_phrase=%s",
                trace_id,
                json.dumps(attrs, ensure_ascii=False),
                pass1_min_sim,
                pass1_top_k,
                is_brand_phrase,
            )
            retrieval_payload = generator.get_embedding_filter_by_attributes(
                attributes=attrs,
                query_text=message_for_intent,
                platform=payload.platform,
                tenant_id=payload.tenant_id,
                locale=payload.locale,
                store_code=payload.store_code,
                min_similarity=pass1_min_sim,
                top_k=pass1_top_k,
                attribute_min_similarity=None,
            )
            if isinstance(retrieval_payload, dict):
                incoming_filters = _normalize_filters(retrieval_payload.get("selected_filters", []))
            logger.info("[chat_turn:%s] incoming_filters pass1=%s", trace_id, json.dumps(_flatten_filters(incoming_filters), ensure_ascii=False))

            # Fallback semántico compuesto en chat_turn:
            # hacemos una segunda recuperación con la query completa como "atributo",
            # y mergeamos resultados para cubrir misses del extractor de intent.
            if message_for_intent.strip() != "":
                # En fallback con query completa, evitamos "ruido" subiendo min_similarity y
                # limitando top_k para no traer filtros irrelevantes.
                if is_brand_phrase:
                    fb_min_sim = max(payload.min_similarity, 0.75)
                    fb_top_k = 3
                else:
                    fb_min_sim = min(payload.min_similarity, 0.65)
                    fb_top_k = max(payload.top_k, 8)

                logger.info(
                    "[chat_turn:%s] retrieval fallback attrs=[full_query] min_similarity=%s top_k=%s is_brand_phrase=%s",
                    trace_id,
                    fb_min_sim,
                    fb_top_k,
                    is_brand_phrase,
                )
                fallback_retrieval_payload = generator.get_embedding_filter_by_attributes(
                    attributes=[message_for_intent],
                    query_text=message_for_intent,
                    platform=payload.platform,
                    tenant_id=payload.tenant_id,
                    locale=payload.locale,
                    store_code=payload.store_code,
                    min_similarity=fb_min_sim,
                    top_k=fb_top_k,
                    attribute_min_similarity=None,
                )
                if isinstance(fallback_retrieval_payload, dict):
                    fallback_filters = _normalize_filters(
                        fallback_retrieval_payload.get("selected_filters", [])
                    )
                    logger.info("[chat_turn:%s] fallback_filters=%s", trace_id, json.dumps(_flatten_filters(fallback_filters), ensure_ascii=False))
                    if fallback_filters:
                        incoming_filters = _merge_filters(incoming_filters, fallback_filters, "add", message=payload.message)
                        logger.info(
                            "[chat_turn:%s] incoming_filters merged_with_fallback=%s",
                            trace_id,
                            json.dumps(_flatten_filters(incoming_filters), ensure_ascii=False),
                        )
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

    merged_filters = _merge_filters(previous_filters, incoming_filters, operation, message=payload.message)
    logger.info("[chat_turn:%s] merged_filters=%s", trace_id, json.dumps(_flatten_filters(merged_filters), ensure_ascii=False))
    detected_intent = _detect_intent(payload.message, merged_filters, operation)

    search_text_message = message_for_intent if compound_keep_segment != "" else payload.message
    search_text = _build_search_text(
        previous_search_text=str(previous.get("search_text", "")),
        message=search_text_message,
        operation=operation,
    )
    logger.info("[chat_turn:%s] search_text_message=%r -> search_text=%r", trace_id, search_text_message, search_text)

    explanation = _build_explanation(
        operation,
        merged_filters,
        detected_intent,
        response_payload=response_payload,
        is_compound_replace_after_remove=(is_compound and operation == "replace"),
    )

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


@chat_turn_router.post("/", tags=["Chat"])
def chat_turn(payload: ChatTurnIn):
    return _handle_chat_turn(payload)


@chat_turn_router.post("", tags=["Chat"])
def chat_turn_no_trailing_slash(payload: ChatTurnIn):
    return _handle_chat_turn(payload)
