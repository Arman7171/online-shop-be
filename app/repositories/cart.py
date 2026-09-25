from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.cart import CartModel
from app.models.cart_item import CartItemModel


class CartRepository:

    @staticmethod
    async def get_by_user_id(
        db: AsyncSession,
        user_id: int,
    ) -> CartModel | None:
        result = await db.execute(
            select(CartModel)
            .options(
                selectinload(CartModel.items)
                .selectinload(CartItemModel.product)
            )
            .where(
                CartModel.user_id == user_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def create(
        db: AsyncSession,
        user_id: int,
    ) -> CartModel:
        cart = CartModel(
            user_id=user_id,
        )

        db.add(cart)

        await db.commit()
        await db.refresh(cart)

        return cart

    @staticmethod
    async def get_item(
        db: AsyncSession,
        cart_id: int,
        product_id: int,
    ) -> CartItemModel | None:
        result = await db.execute(
            select(CartItemModel).where(
                CartItemModel.cart_id == cart_id,
                CartItemModel.product_id == product_id,
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def add_item(
        db: AsyncSession,
        cart_id: int,
        product_id: int,
        quantity: int,
    ) -> CartItemModel:
        item = CartItemModel(
            cart_id=cart_id,
            product_id=product_id,
            quantity=quantity,
        )

        db.add(item)

        await db.commit()
        await db.refresh(item)

        return item

    @staticmethod
    async def update_item_quantity(
        db: AsyncSession,
        item: CartItemModel,
        quantity: int,
    ) -> CartItemModel:
        item.quantity = quantity

        await db.commit()
        await db.refresh(item)

        return item

    @staticmethod
    async def delete_item(
        db: AsyncSession,
        item: CartItemModel,
    ) -> None:
        await db.delete(item)
        await db.commit()