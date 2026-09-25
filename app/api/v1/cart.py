from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import UserModel
from app.schemas.cart import AddCartItem, CartResponse, UpdateCartItem
from app.services.cart import CartService


router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)


@router.get(
    "",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def get_cart(
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return await CartService.get_cart(
        db=db,
        user_id=current_user.id,
    )

@router.post(
    "/items",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def add_item_to_cart(
    data: AddCartItem,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return await CartService.add_item(
        db=db,
        user_id=current_user.id,
        data=data,
    )

@router.patch(
    "/items/{item_id}",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def update_cart_item(
    item_id: int,
    data: UpdateCartItem,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return await CartService.update_item(
        db=db,
        user_id=current_user.id,
        item_id=item_id,
        data=data,
    )

@router.delete(
    "/items/{item_id}",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_cart_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return await CartService.delete_item(
        db=db,
        user_id=current_user.id,
        item_id=item_id,
    )