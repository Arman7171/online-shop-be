from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product_image import ProductImageModel
from app.repositories.product import ProductRepository
from app.repositories.product_image import ProductImageRepository


UPLOAD_DIR = Path("uploads/products")

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


class ProductImageService:

    @staticmethod
    async def create(
        db: AsyncSession,
        product_id: int,
        file: UploadFile,
    ) -> ProductImageModel:

        product = await ProductRepository.get_by_id(
            db=db,
            product_id=product_id,
        )

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        if file.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only JPEG, PNG and WEBP images are allowed",
            )

        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file name",
            )

        UPLOAD_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        extension = Path(file.filename).suffix.lower()

        file_name = f"{uuid4()}{extension}"

        file_path = UPLOAD_DIR / file_name

        file_content = await file.read()

        with open(file_path, "wb") as image_file:
            image_file.write(file_content)

        image_url = f"/uploads/products/{file_name}"

        return await ProductImageRepository.create(
            db=db,
            product_id=product_id,
            url=image_url,
        )