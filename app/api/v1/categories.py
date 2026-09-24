from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_admin
from app.database import get_db
from app.models.user import UserModel
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.services.category import CategoryService


router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    _: UserModel = Depends(get_current_admin),
):
    return await CategoryService.create(
        db=db,
        data=data,
    )

@router.get(
    "/",
    response_model=list[CategoryResponse],
)
async def get_all_categories(
    db: AsyncSession = Depends(get_db),
):
    return await CategoryService.get_all(db)

@router.get(
    "/{slug}",
    response_model=CategoryResponse,
)
async def get_category_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_db),
):
    return await CategoryService.get_category_by_slug(
        db=db,
        slug=slug,
    )

@router.patch(
    "/{category_id}",
    response_model=CategoryResponse,
)
async def update_category(
    category_id: int,
    data: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
):
    return await CategoryService.update(
        db=db,
        category_id = category_id,
        data=data,
    )

@router.delete(
    "/{category_id}",
)
async def delete(
    category_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await CategoryService.delete(
        db=db,
         category_id = category_id,
    )