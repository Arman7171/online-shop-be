from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProductImageCreate(BaseModel):
    url: str = Field(
        min_length=1,
        max_length=500,
    )

    is_primary: bool = False

    position: int = Field(
        default=0,
        ge=0,
    )

    model_config = ConfigDict(
        extra="forbid"
    )


class ProductImageResponse(BaseModel):
    id: int
    product_id: int
    url: str
    is_primary: bool
    position: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )