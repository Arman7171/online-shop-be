from app.schemas.category import CategoryCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.category import CategoryModel

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