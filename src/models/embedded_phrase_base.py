from pydantic import BaseModel, Field, field_validator


class EmbeddedPhraseUploadBase(BaseModel):
    platform: str = Field(default="magento", min_length=1)
    tenant_id: str = Field(default="default", min_length=1)
    locale: str = Field(default="es_AR", min_length=2)
    store_code: str = Field(default="default", min_length=1)
    attribute_code: str
    attribute_value_string: str = ''
    attribute_value_number: int | float | None = None
    phrase: str
