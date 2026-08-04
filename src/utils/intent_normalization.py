from typing import Any


def to_number_or_none(value: Any):
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


def _first_numeric(payload: dict, keys: list[str]):
    for key in keys:
        numeric = to_number_or_none(payload.get(key))
        if numeric is not None:
            return numeric
    return None


def normalize_response_block(
    response_payload: Any,
    numeric_aliases: dict[str, list[str]] | None = None,
) -> dict:
    payload = response_payload if isinstance(response_payload, dict) else {}
    numeric_aliases = numeric_aliases or {}
    characteristics = payload.get("characteristics", [])
    if not isinstance(characteristics, list):
        characteristics = []

    domain_filters_payload = payload.get("domain_filters", {})
    domain_filters: dict[str, int | float] = {}
    if isinstance(domain_filters_payload, dict):
        for key, value in domain_filters_payload.items():
            clean_key = str(key).strip()
            if clean_key == "":
                continue
            numeric = to_number_or_none(value)
            if numeric is not None:
                domain_filters[clean_key] = numeric

    canonical_numeric_fields = [
        "price_min",
        "price_max",
        "min_battery_mah",
        "min_ram_gb",
        "min_storage_gb",
    ]

    normalized_numeric = {}
    for field in canonical_numeric_fields:
        alias_keys = [field]
        alias_keys.extend(numeric_aliases.get(field, []))
        normalized_numeric[field] = _first_numeric(payload, alias_keys)

    return {
        "price_min": normalized_numeric["price_min"],
        "price_max": normalized_numeric["price_max"],
        "min_battery_mah": normalized_numeric["min_battery_mah"],
        "min_ram_gb": normalized_numeric["min_ram_gb"],
        "min_storage_gb": normalized_numeric["min_storage_gb"],
        "characteristics": [str(c).strip() for c in characteristics if str(c).strip() != ""],
        "domain_filters": domain_filters,
    }
