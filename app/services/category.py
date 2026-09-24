from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from slugify import slugify

from app.models.category import CategoryModel
from app.repositories.category import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:

    @staticmethod
    async def create(
        db: AsyncSession,
        data: CategoryCreate,
    ) -> CategoryModel:

        existing_category = await CategoryRepository.get_by_name(
            db=db,
            name=data.name,
        )

        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category with this name already exists",
            )

        slug = slugify(data.name)

        existing_slug = await CategoryRepository.get_by_slug(
            db=db,
            slug=slug,
        )

        if existing_slug:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category with this slug already exists",
            )

        return await CategoryRepository.create(
            db=db,
            data=data,
            slug=slug,
        )

    @staticmethod
    async def get_all(db: AsyncSession):
        return await CategoryRepository.get_all(db)

    @staticmethod
    async def get_category_by_slug(db: AsyncSession, slug: str):
        category = await CategoryRepository.get_by_slug(db, slug)
        if not category:
            raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="category by this slug not found",
                    )
        return category 

    @staticmethod
    async def update(
        db: AsyncSession,
        category_id: int,
        data: CategoryUpdate,
    ) -> CategoryModel:

        category = await CategoryRepository.get_by_id(
            db=db,
            category_id=category_id,
        )

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "name" in update_data:
            existing_category = await CategoryRepository.get_by_name(
                db=db,
                name=update_data["name"],
            )

            if existing_category and existing_category.id != category.id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Category with this name already exists",
                )

            new_slug = slugify(update_data["name"])

            existing_slug = await CategoryRepository.get_by_slug(
                db=db,
                slug=new_slug,
            )

            if existing_slug and existing_slug.id != category.id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Category with this slug already exists",
                )

            update_data["slug"] = new_slug

        return await CategoryRepository.update(
            db=db,
            category=category,
            update_data=update_data,
        )

    @staticmethod
    async def delete(db: AsyncSession, category_id: int):
        category = await CategoryRepository.get_by_id(
                db=db,
                category_id=category_id,
            )
    
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

        await CategoryRepository.delete(
        db=db,
        category=category,
    )

        return {
            "message": "Category deleted successfully"
        }

        