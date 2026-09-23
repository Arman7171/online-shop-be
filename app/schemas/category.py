from pydantic import BaseModel, Field, field_validator, ConfigDict

class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, min_length=1)
    is_active: bool = True

    model_config = ConfigDict(extra="forbid")
