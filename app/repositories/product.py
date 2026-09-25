from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.product import ProductCreate
from app.models.product import ProductModel
from sqlalchemy import select
from sqlalchemy.orm import selectinload

class ProductRepository:

    @staticmethod
    async def create(
        db: AsyncSession,
        data: ProductCreate,
        slug: str,
    ) -> ProductModel:
        product = ProductModel(
            name=data.name,
            description=data.description,
            price=data.price,
            stock=data.stock,
            category_id=data.category_id,
            is_active=data.is_active,
            slug=slug,
        )

        db.add(product)

        await db.commit()

        created_product = await ProductRepository.get_by_id(
            db=db,
            product_id=product.id,
        )

        if created_product is None:
            raise RuntimeError("Created product could not be loaded")

        return created_product

    @staticmethod
    async def get_by_id(db: AsyncSession, product_id: int) -> ProductModel | None:
        result = await db.execute(
            select(ProductModel)
            .where(ProductModel.id == product_id)
            .options(
                selectinload(ProductModel.images)
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_slug(
        db: AsyncSession,
        product_slug: str,
    ) -> ProductModel | None:
        result = await db.execute(
            select(ProductModel)
            .options(
                selectinload(ProductModel.images)
            )
            .where(
                ProductModel.slug == product_slug
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(db: AsyncSession) -> list[ProductModel]:
        result = await db.execute(
            select(ProductModel)
            .options(
                selectinload(ProductModel.images)
            )
        )

        return list(result.scalars().all())

    @staticmethod
    async def update(
        db: AsyncSession,
        product: ProductModel,
        update_data: dict,
    ) -> ProductModel:

        for field, value in update_data.items():
            setattr(product, field, value)

        await db.commit()

        result = await db.execute(
            select(ProductModel)
            .options(
                selectinload(ProductModel.images)
            )
            .where(
                ProductModel.id == product.id
            )
        )

        return result.scalar_one()

    @staticmethod
    async def delete(
        db: AsyncSession,
        product: ProductModel,
    ) -> None:
        await db.delete(product)
        await db.commit()