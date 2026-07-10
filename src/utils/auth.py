import os

from fastapi import Header, HTTPException


def require_admin_api_key(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> None:
    configured_key = os.getenv("ADMIN_API_KEY", "").strip()

    # Backward-compatible rollout: if no key is configured yet, do not block traffic.
    if configured_key == "":
        return

    if x_api_key != configured_key:
        raise HTTPException(status_code=401, detail="invalid_api_key")