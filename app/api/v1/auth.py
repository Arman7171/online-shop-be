from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.user import RegisterForm, UserResponse
from app.services.user import UserService
from app.schemas.user import (
    RegisterForm,
    UserResponse,
    VerifyEmailForm,
)
from app.schemas.user import ResendVerificationCodeForm

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    data: RegisterForm,
    db: AsyncSession = Depends(get_db),
):
    return await UserService.register(
        db=db,
        data=data,
    )

@router.post(
    "/verify-email",
    response_model=UserResponse,
)
async def verify_email(
    data: VerifyEmailForm,
    db: AsyncSession = Depends(get_db),
):
    return await UserService.verify_email(
        db=db,
        data=data,
    )

@router.post("/resend-verification-code")
async def resend_verification_code(
    data: ResendVerificationCodeForm,
    db: AsyncSession = Depends(get_db),
):
    return await UserService.resend_verification_code(
        db=db,
        data=data,
    )