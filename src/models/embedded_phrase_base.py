from pydantic import BaseModel, Field, field_validator

from src.utils.scope_config import (
    DEFAULT_LOCALE,
    DEFAULT_PLATFORM,
    DEFAULT_STORE_CODE,
    DEFAULT_TENANT_ID,
)


class EmbeddedPhraseUploadBase(BaseModel):
    platform: str = Field(default=DEFAULT_PLATFORM, min_length=1)
    tenant_id: str = Field(default=DEFAULT_TENANT_ID, min_length=1)
    locale: str = Field(default=DEFAULT_LOCALE, min_length=2)
    store_code: str = Field(default=DEFAULT_STORE_CODE, min_length=1)
    attribute_code: str
    attribute_value_string: str = ''
    attribute_value_number: int | float | None = None
    phrase: str
