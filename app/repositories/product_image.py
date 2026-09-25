from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product_image import ProductImageModel


class ProductImageRepository:

    @staticmethod
    async def create(
        db: AsyncSession,
        product_id: int,
        url: str,
    ) -> ProductImageModel:

        image = ProductImageModel(
            product_id=product_id,
            url=url,
        )

        db.add(image)

        await db.commit()
        await db.refresh(image)

        return image