from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class AddCartItem(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(default=1, ge=1)

    model_config = ConfigDict(
        extra="forbid"
    )


class UpdateCartItem(BaseModel):
    quantity: int = Field(ge=1)

    model_config = ConfigDict(
        extra="forbid"
    )


class CartProductResponse(BaseModel):
    id: int
    name: str
    slug: str
    price: Decimal
    stock: int

    model_config = ConfigDict(
        from_attributes=True
    )


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    product: CartProductResponse

    model_config = ConfigDict(
        from_attributes=True
    )


class CartResponse(BaseModel):
    id: int
    user_id: int
    items: list[CartItemResponse] = []

    model_config = ConfigDict(
        from_attributes=True
    )