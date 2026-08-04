import json
import os
from typing import Any

from src.utils.scope_config import resolve_scoped_env

ALLOWED_DOMAIN_PROFILES = {"generic", "electronics"}
DEFAULT_DOMAIN_PROFILE = os.getenv("AI_DOMAIN_PROFILE", "generic").strip().lower() or "generic"


def normalize_domain_profile(profile: str | None) -> str:
    value = "" if profile is None else str(profile).strip().lower()
    if value in ALLOWED_DOMAIN_PROFILES:
        return value
    return "generic"


def resolve_domain_profile(
    platform: str,
    tenant_id: str,
    locale: str,
    store_code: str,
) -> str:
    configured = resolve_scoped_env(
        base="INTENT_DOMAIN_PROFILE",
        platform=platform,
        tenant_id=tenant_id,
        locale=locale,
        store_code=store_code,
        default=DEFAULT_DOMAIN_PROFILE,
    )
    return normalize_domain_profile(configured)


def resolve_numeric_aliases(
    platform: str,
    tenant_id: str,
    locale: str,
    store_code: str,
) -> dict[str, list[str]]:
    raw = resolve_scoped_env(
        base="INTENT_NUMERIC_FIELD_ALIASES",
        platform=platform,
        tenant_id=tenant_id,
        locale=locale,
        store_code=store_code,
        default="{}",
    )

    try:
        parsed = json.loads(raw)
    except Exception:
        return {}

    if not isinstance(parsed, dict):
        return {}

    aliases: dict[str, list[str]] = {}
    for key, value in parsed.items():
        canonical = str(key).strip()
        if canonical == "":
            continue

        values: list[Any]
        if isinstance(value, list):
            values = value
        else:
            values = [value]

        cleaned = []
        for item in values:
            alias = str(item).strip()
            if alias != "":
                cleaned.append(alias)

        if cleaned:
            aliases[canonical] = cleaned

    return aliases
