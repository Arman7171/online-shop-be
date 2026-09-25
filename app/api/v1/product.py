from fastapi import APIRouter, Depends, status
from app.schemas.product import ProductCreate, ProductUpdate
from app.services.product import ProductService 
from app.core.dependencies import get_current_admin
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.product import ProductResponse
from app.schemas.product_image import (
    ProductImageCreate,
    ProductImageResponse,
)
from app.services.product_image import ProductImageService
from app.models.user import UserModel
from fastapi import File, UploadFile

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)

@router.post(
        "/",
        response_model=ProductResponse,
        status_code=status.HTTP_201_CREATED,
    )
async def create(data: ProductCreate, db: AsyncSession = Depends(get_db), _: UserModel = Depends(get_current_admin)):
    return await ProductService.create(db, data=data)

@router.post(
    "/{product_id}/images",
    response_model=ProductImageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_product_image(
    product_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    _: UserModel = Depends(get_current_admin),
):
    return await ProductImageService.create(
        db=db,
        product_id=product_id,
        file=file,
    )

@router.get(
    "/{slug}",
    response_model=ProductResponse,
)
async def get_product_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_db),
):
    return await ProductService.get_product_by_slug(
        db=db,
        slug=slug,
    )

@router.get(
    "/",
    response_model=list[ProductResponse],
)
async def get_all_products(
    db: AsyncSession = Depends(get_db),
):
    return await ProductService.get_all_products(
        db=db,
    )

@router.patch(
    "/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
)
async def update_product(
    product_id: int,
    data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    _: UserModel = Depends(get_current_admin),
):
    return await ProductService.update(
        db=db,
        product_id=product_id,
        data=data,
    )

@router.delete(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    _: UserModel = Depends(get_current_admin),
):
    return await ProductService.delete(
        db=db,
        product_id=product_id,
    )