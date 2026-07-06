from pydantic import BaseModel, Field, field_validator


class EmbeddedPhraseUploadBase(BaseModel):
    attribute_code: str
    attribute_value_string: str = ''
    attribute_value_number: int | float | None = None
    phrase: str
