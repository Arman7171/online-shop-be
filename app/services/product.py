from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.product import ProductCreate, ProductUpdate
from app.repositories.product import ProductRepository
from app.repositories.category import CategoryRepository
from app.models.product import ProductModel
from fastapi import HTTPException, status
from slugify import slugify

class ProductService:

    @staticmethod
    async def create(db: AsyncSession, data: ProductCreate):
        
        slug = slugify(data.name)

        existed_product = ProductRepository.get_by_slug(db, slug)

        if not existed_product:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="product with this slug already exists",
            )

        return await ProductRepository.create(db=db, data=data, slug=slug)

    @staticmethod
    async def get_product_by_slug(db: AsyncSession, slug: str):
        product = await ProductRepository.get_by_slug(db=db, product_slug=slug)
        if not product:
            raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="product by this slug not found",
                    )
        return product 

    @staticmethod
    async def get_all_products(db: AsyncSession):
        return await ProductRepository.get_all(db)

    @staticmethod
    async def update(
        db: AsyncSession,
        product_id: int,
        data: ProductUpdate,
    ) -> ProductModel:

        product = await ProductRepository.get_by_id(
            db=db,
            product_id=product_id,
        )

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "category_id" in update_data:
            category = await CategoryRepository.get_by_id(
                db=db,
                category_id=update_data["category_id"],
            )

            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Category not found",
                )

        if "name" in update_data:
            new_slug = slugify(
                update_data["name"]
            )

            existing_product = await ProductRepository.get_by_slug(
                db=db,
                product_slug=new_slug,
            )

            if (
                existing_product
                and existing_product.id != product.id
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Product with this slug already exists",
                )

            update_data["slug"] = new_slug

        return await ProductRepository.update(
            db=db,
            product=product,
            update_data=update_data,
        )

    @staticmethod
    async def delete(
        db: AsyncSession,
        product_id: int,
    ) -> dict:
        product = await ProductRepository.get_by_id(
            db=db,
            product_id=product_id,
        )

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        await ProductRepository.delete(
            db=db,
            product=product,
        )

        return {
            "message": "Product deleted successfully"
        }