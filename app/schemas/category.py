from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, min_length=1)
    is_active: bool = True

    model_config = ConfigDict(extra="forbid")



class CategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class CategoryUpdate(BaseModel):
    name: str | None = Field(min_length=1, max_length=100, default=None)
    description: str | None = Field(default=None, min_length=1)
    is_active: bool | None = None

    model_config = ConfigDict(extra="forbid")