from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.order import OrderModel
from app.models.order_item import OrderItemModel


class OrderRepository:

    @staticmethod
    async def create_order(
        db: AsyncSession,
        user_id: int,
        total_amount,
        status: str = "pending",
    ) -> OrderModel:
        order = OrderModel(
            user_id=user_id,
            total_amount=total_amount,
            status=status,
        )

        db.add(order)

        await db.flush()

        return order

    @staticmethod
    async def create_order_item(
        db: AsyncSession,
        order_id: int,
        product_id: int,
        product_name: str,
        price,
        quantity: int,
        subtotal,
    ) -> OrderItemModel:
        item = OrderItemModel(
            order_id=order_id,
            product_id=product_id,
            product_name=product_name,
            price=price,
            quantity=quantity,
            subtotal=subtotal,
        )

        db.add(item)

        await db.flush()

        return item

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        order_id: int,
    ) -> OrderModel | None:
        result = await db.execute(
            select(OrderModel)
            .options(
                selectinload(OrderModel.items)
            )
            .where(
                OrderModel.id == order_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_user_id(
        db: AsyncSession,
        user_id: int,
    ) -> list[OrderModel]:
        result = await db.execute(
            select(OrderModel)
            .options(
                selectinload(OrderModel.items)
            )
            .where(
                OrderModel.user_id == user_id
            )
            .order_by(
                OrderModel.created_at.desc()
            )
        )

        return list(result.scalars().all())