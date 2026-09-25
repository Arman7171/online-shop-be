from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cart import CartModel
from app.repositories.cart import CartRepository
from app.repositories.product import ProductRepository
from app.schemas.cart import AddCartItem, UpdateCartItem


class CartService:

    @staticmethod
    async def add_item(
        db: AsyncSession,
        user_id: int,
        data: AddCartItem,
    ) -> CartModel:

        product = await ProductRepository.get_by_id(
            db=db,
            product_id=data.product_id,
        )

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        if not product.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product is not available",
            )

        if product.stock <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product is out of stock",
            )

        cart = await CartRepository.get_by_user_id(
            db=db,
            user_id=user_id,
        )

        if not cart:
            cart = await CartRepository.create(
                db=db,
                user_id=user_id,
            )

        existing_item = await CartRepository.get_item(
            db=db,
            cart_id=cart.id,
            product_id=data.product_id,
        )

        if existing_item:
            new_quantity = (
                existing_item.quantity + data.quantity
            )

            if new_quantity > product.stock:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Only {product.stock} items available",
                )

            await CartRepository.update_item_quantity(
                db=db,
                item=existing_item,
                quantity=new_quantity,
            )

        else:
            if data.quantity > product.stock:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Only {product.stock} items available",
                )

            await CartRepository.add_item(
                db=db,
                cart_id=cart.id,
                product_id=data.product_id,
                quantity=data.quantity,
            )

        updated_cart = await CartRepository.get_by_user_id(
            db=db,
            user_id=user_id,
        )

        if not updated_cart:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Cart could not be loaded",
            )

        return updated_cart

    @staticmethod
    async def get_cart(
        db: AsyncSession,
        user_id: int,
    ) -> CartModel:
        cart = await CartRepository.get_by_user_id(
            db=db,
            user_id=user_id,
        )

        if not cart:
            cart = await CartRepository.create(
                db=db,
                user_id=user_id,
            )

            cart = await CartRepository.get_by_user_id(
                db=db,
                user_id=user_id,
            )

        if not cart:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Cart could not be loaded",
            )

        return cart

    @staticmethod
    async def update_item(
        db: AsyncSession,
        user_id: int,
        item_id: int,
        data: UpdateCartItem,
    ) -> CartModel:
        cart = await CartRepository.get_by_user_id(
            db=db,
            user_id=user_id,
        )

        if not cart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart not found",
            )

        item = next(
            (
                item
                for item in cart.items
                if item.id == item_id
            ),
            None,
        )

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found",
            )

        product = await ProductRepository.get_by_id(
            db=db,
            product_id=item.product_id,
        )

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        if data.quantity > product.stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Only {product.stock} items available",
            )

        await CartRepository.update_item_quantity(
            db=db,
            item=item,
            quantity=data.quantity,
        )

        updated_cart = await CartRepository.get_by_user_id(
            db=db,
            user_id=user_id,
        )

        if not updated_cart:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Cart could not be loaded",
            )

        return updated_cart

    @staticmethod
    async def delete_item(
        db: AsyncSession,
        user_id: int,
        item_id: int,
    ) -> CartModel:
        cart = await CartRepository.get_by_user_id(
            db=db,
            user_id=user_id,
        )

        if not cart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart not found",
            )

        item = next(
            (
                item
                for item in cart.items
                if item.id == item_id
            ),
            None,
        )

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found",
            )

        await CartRepository.delete_item(
            db=db,
            item=item,
        )

        updated_cart = await CartRepository.get_by_user_id(
            db=db,
            user_id=user_id,
        )

        if not updated_cart:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Cart could not be loaded",
            )

        return updated_cart 