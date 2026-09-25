from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.product_image import ProductImageResponse

class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: str | None = Field(default=None, min_length=1)
    price: Decimal = Field(gt=0)
    stock: int = Field(default=0, ge=0)
    category_id: int = Field(gt=0)
    is_active: bool = True

    model_config = ConfigDict(extra="forbid")

class ProductUpdate(BaseModel):
    name: str | None = Field(min_length=1, max_length=150, default=None)
    description: str | None = Field(min_length=1, default=None)
    price: Decimal | None = Field(gt=0, default=None)
    stock: int | None = Field(ge=0, default=None)
    category_id: int | None = Field(gt=0, default=None)
    is_active: bool | None = None

    model_config = ConfigDict(extra="forbid")

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: Decimal
    stock: int
    slug: str
    category_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    images: list[ProductImageResponse] = []

    model_config = ConfigDict(
        from_attributes=True
    )