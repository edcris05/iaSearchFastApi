import os


DEFAULT_PLATFORM = os.getenv("API_DEFAULT_PLATFORM", "ecommerce").strip() or "ecommerce"
DEFAULT_TENANT_ID = os.getenv("API_DEFAULT_TENANT_ID", "default").strip() or "default"
DEFAULT_LOCALE = os.getenv("API_DEFAULT_LOCALE", "es").strip() or "es"
DEFAULT_STORE_CODE = os.getenv("API_DEFAULT_STORE_CODE", "default").strip() or "default"


def _scope_part(value: str | None) -> str:
    text = "" if value is None else str(value).strip().lower()
    if text == "":
        return "DEFAULT"

    normalized = "".join(ch if ch.isalnum() else "_" for ch in text)
    while "__" in normalized:
        normalized = normalized.replace("__", "_")

    normalized = normalized.strip("_")
    return normalized.upper() if normalized != "" else "DEFAULT"


def scoped_env_names(
    base: str,
    platform: str,
    tenant_id: str,
    locale: str,
    store_code: str,
) -> list[str]:
    p = _scope_part(platform)
    t = _scope_part(tenant_id)
    l = _scope_part(locale)
    s = _scope_part(store_code)

    return [
        f"{base}__{p}",
        f"{base}__{p}__{t}",
        f"{base}__{p}__{t}__{l}",
        f"{base}__{p}__{t}__{l}__{s}",
    ]


def resolve_scoped_env(
    base: str,
    platform: str,
    tenant_id: str,
    locale: str,
    store_code: str,
    default: str = "",
) -> str:
    value = os.getenv(base, default).strip()

    for env_name in scoped_env_names(
        base=base,
        platform=platform,
        tenant_id=tenant_id,
        locale=locale,
        store_code=store_code,
    ):
        scoped_value = os.getenv(env_name, "").strip()
        if scoped_value != "":
            value = scoped_value

    return value
