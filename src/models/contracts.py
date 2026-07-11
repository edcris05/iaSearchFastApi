from pydantic import BaseModel, ConfigDict, Field
from typing import Any


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CorrectionCreate(StrictBaseModel):
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


class CorrectionUpdate(StrictBaseModel):
    locale: str | None = None
    attribute_code: str | None = None
    raw_phrase: str | None = None
    corrected_value_string: str | None = None
    corrected_value_number: int | float | None = None
    rule_type: str | None = Field(default=None, pattern="^(exact|contains|regex)$")
    priority: int | None = None
    is_active: bool | None = None
    changed_by: str = "system"


class SearchEventIn(StrictBaseModel):
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


class SearchIntentResponse(StrictBaseModel):
    price_min: int | float | None = None
    price_max: int | float | None = None
    min_battery_mah: int | float | None = None
    min_ram_gb: int | float | None = None
    min_storage_gb: int | float | None = None
    characteristics: list[str] = []


class RetrievalCandidateOut(StrictBaseModel):
    attribute_code: str
    attribute_value_string: str = ""
    attribute_value_number: int | float | None = None
    phrase: str = ""
    similarity: float


class RetrievalConfidenceOut(StrictBaseModel):
    top_similarity: float
    second_similarity: float | None = None
    margin: float | None = None
    confidence_band: str


class RetrievalAttributeOut(StrictBaseModel):
    attribute_code: str
    selected: RetrievalCandidateOut
    top_k: list[RetrievalCandidateOut] = []
    confidence: RetrievalConfidenceOut


class RetrievalOut(StrictBaseModel):
    strategy: str = "top_k_per_attribute"
    top_k: int
    min_similarity: float
    attributes: list[RetrievalAttributeOut] = []


class AppliedCorrectionOut(StrictBaseModel):
    correction_id: int
    attribute_code: str
    raw_phrase: str
    old_value_string: str
    old_value_number: int | float | None = None
    new_value_string: str
    new_value_number: int | float | None = None
    rule_type: str
    priority: int


class SearchResponseMeta(StrictBaseModel):
    api_version: str
    request_id: str
    source: str
    fallback_reason: str | None = None
    latency_ms: int
    platform: str
    tenant_id: str
    locale: str
    store_code: str


class SearchResponseOut(StrictBaseModel):
    response: SearchIntentResponse
    input_tokens: int
    output_tokens: int
    total_tokens: int
    filters: list[list[tuple[str, str, int | float | None, str, float]]] = []
    retrieval: RetrievalOut
    applied_corrections: list[AppliedCorrectionOut] = []
    meta: SearchResponseMeta
