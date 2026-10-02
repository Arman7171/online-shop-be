from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cart_item import CartItemModel
from app.models.order import OrderModel
from app.models.product import ProductModel
from app.repositories.cart import CartRepository
from app.repositories.order import OrderRepository


class OrderService:

    @staticmethod
    async def checkout(
        db: AsyncSession,
        user_id: int,
    ) -> OrderModel:
        try:
            # 1. Получаем корзину пользователя
            cart = await CartRepository.get_by_user_id(
                db=db,
                user_id=user_id,
            )

            if not cart:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cart not found",
                )

            if not cart.items:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cart is empty",
                )

            # 2. Получаем ID всех товаров из корзины
            product_ids = sorted(
                item.product_id
                for item in cart.items
            )

            # 3. Блокируем товары до конца transaction
            result = await db.execute(
                select(ProductModel)
                .where(
                    ProductModel.id.in_(product_ids)
                )
                .order_by(ProductModel.id)
                .with_for_update()
            )

            products = list(result.scalars().all())

            products_by_id = {
                product.id: product
                for product in products
            }

            # 4. Проверяем stock и считаем total
            total_amount = Decimal("0.00")

            for cart_item in cart.items:
                product = products_by_id.get(
                    cart_item.product_id
                )

                if not product:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Product {cart_item.product_id} not found",
                    )

                if not product.is_active:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"{product.name} is not available",
                    )

                if cart_item.quantity > product.stock:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=(
                            f"Not enough stock for {product.name}. "
                            f"Available: {product.stock}"
                        ),
                    )

                subtotal = (
                    product.price
                    * cart_item.quantity
                )

                total_amount += subtotal

            # 5. Создаём order
            order = await OrderRepository.create_order(
                db=db,
                user_id=user_id,
                total_amount=total_amount,
                status="pending",
            )

            # 6. Создаём order items
            #    и уменьшаем stock
            for cart_item in cart.items:
                product = products_by_id[
                    cart_item.product_id
                ]

                subtotal = (
                    product.price
                    * cart_item.quantity
                )

                await OrderRepository.create_order_item(
                    db=db,
                    order_id=order.id,
                    product_id=product.id,
                    product_name=product.name,
                    price=product.price,
                    quantity=cart_item.quantity,
                    subtotal=subtotal,
                )

                product.stock -= cart_item.quantity

            # 7. Очищаем cart
            await db.execute(
                delete(CartItemModel).where(
                    CartItemModel.cart_id == cart.id
                )
            )

            # 8. Всё прошло успешно
            await db.commit()

            # 9. Получаем готовый order вместе с items
            created_order = await OrderRepository.get_by_id(
                db=db,
                order_id=order.id,
            )

            if created_order is None:
                raise RuntimeError(
                    "Created order could not be loaded"
                )

            return created_order

        except HTTPException:
            await db.rollback()
            raise

        except Exception:
            await db.rollback()
            raise