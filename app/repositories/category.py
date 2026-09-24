from app.schemas.category import CategoryCreate, CategoryUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.category import CategoryModel
from sqlalchemy import select, update
class CategoryRepository:

    @staticmethod
    async def create(
        db: AsyncSession,
        data: CategoryCreate,
        slug: str,
    ) -> CategoryModel:

        category = CategoryModel(
            name=data.name, 
            slug=slug,
            description=data.description,
            is_active=data.is_active,
        )

        db.add(category)

        await db.commit()
        await db.refresh(category)

        return category

    @staticmethod
    async def get_by_name(
        db: AsyncSession,
        name: str,
    ) -> CategoryModel | None:
        result = await db.execute(
            select(CategoryModel).where(
                CategoryModel.name == name
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        category_id: int,
    ) -> CategoryModel | None:
        result = await db.execute(
            select(CategoryModel).where(
                CategoryModel.id == category_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_slug(
        db: AsyncSession,
        slug: str,
    ) -> CategoryModel | None:
        result = await db.execute(
            select(CategoryModel).where(
                CategoryModel.slug == slug
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(db: AsyncSession) -> list[CategoryModel]:
        result = await db.execute(select(CategoryModel))

        return list(result.scalars().all())

    @staticmethod
    async def update(
        db: AsyncSession,
        category: CategoryModel,
        update_data: dict,
    ) -> CategoryModel:

        for field, value in update_data.items():
            setattr(category, field, value)

        await db.commit()
        await db.refresh(category)

        return category

    @staticmethod
    async def delete(
        db: AsyncSession,
        category: CategoryModel,
    ) -> None:
        await db.delete(category)
        await db.commit()