from pydantic import BaseModel, Field
from typing import Any


class CorrectionCreate(BaseModel):
    platform: str = Field(..., min_length=1)
    tenant_id: str = Field(..., min_length=1)
    locale: str = Field(default="es_AR", min_length=2)
    attribute_code: str = Field(..., min_length=1)
    raw_phrase: str = Field(..., min_length=1)
    corrected_value_string: str = ""
    corrected_value_number: int | float | None = None
    rule_type: str = Field(default="exact", pattern="^(exact|contains|regex)$")
    priority: int = 100
    is_active: bool = True
    created_by: str = "system"


class CorrectionUpdate(BaseModel):
    locale: str | None = None
    attribute_code: str | None = None
    raw_phrase: str | None = None
    corrected_value_string: str | None = None
    corrected_value_number: int | float | None = None
    rule_type: str | None = Field(default=None, pattern="^(exact|contains|regex)$")
    priority: int | None = None
    is_active: bool | None = None
    changed_by: str = "system"


class SearchEventIn(BaseModel):
    request_id: str
    platform: str
    tenant_id: str
    session_id: str | None = None
    event_type: str = Field(..., pattern="^(search|result_click|add_to_cart|conversion)$")
    query_text: str | None = None
    source: str | None = None
    fallback_reason: str | None = None
    api_version: str | None = None
    latency_ms: int | None = None
    filters: list[Any] = []
    product_id: str | None = None
    position: int | None = None
