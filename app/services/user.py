from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.core.verification import (
    generate_verification_code,
    hash_verification_code,
)
from app.models.user import UserModel
from app.repositories.user import UserRepository
from app.repositories.verification_code import VerificationCodeRepository
from app.schemas.user import RegisterForm
from app.core.verification import verify_verification_code
from app.schemas.user import VerifyEmailForm
from app.schemas.user import ResendVerificationCodeForm

class UserService:

    @staticmethod
    async def register(
        db: AsyncSession,
        data: RegisterForm,
    ) -> UserModel:

        existing_user = await UserRepository.get_by_email(
            db=db,
            email=data.email,
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )

        hashed_password = hash_password(data.password)

        user = await UserRepository.create(
            db=db,
            email=data.email,
            password_hash=hashed_password,
            first_name=data.first_name,
            last_name=data.last_name,
        )

        verification_code = generate_verification_code()

        verification_code_hash = hash_verification_code(
            verification_code
        )

        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=10
        )

        await VerificationCodeRepository.create(
            db=db,
            user_id=user.id,
            code_hash=verification_code_hash,
            expires_at=expires_at,
        )

        print(
            "Verification code:",
            verification_code,
        )

        return user

    @staticmethod
    async def verify_email(
        db: AsyncSession,
        data: VerifyEmailForm,
    ) -> UserModel:

        user = await UserRepository.get_by_email(
            db=db,
            email=data.email,
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already verified",
            )

        verification_code = (
            await VerificationCodeRepository.get_latest_valid(
                db=db,
                user_id=user.id,
            )
        )

        if not verification_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Verification code is invalid or expired",
            )

        is_valid = verify_verification_code(
            code=data.code,
            code_hash=verification_code.code_hash,
        )

        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid verification code",
            )

        await VerificationCodeRepository.mark_as_used(
            db=db,
            verification_code=verification_code,
        )

        user = await UserRepository.mark_as_verified(
            db=db,
            user=user,
        )

        return user

    @staticmethod
    async def resend_verification_code(
        db: AsyncSession,
        data: ResendVerificationCodeForm,
    ) -> dict:

        user = await UserRepository.get_by_email(
            db=db,
            email=data.email,
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already verified",
            )

        latest_code = await VerificationCodeRepository.get_latest_by_user(
            db=db,
            user_id=user.id,
        )

        if latest_code:
            now = datetime.now(timezone.utc)

            next_allowed_time = (
                latest_code.created_at
                + timedelta(seconds=60)
            )

            if now < next_allowed_time:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Please wait before requesting another code",
                )

        await VerificationCodeRepository.invalidate_all_active(
            db=db,
            user_id=user.id,
        )

        code = generate_verification_code()

        code_hash = hash_verification_code(code)

        expires_at = (
            datetime.now(timezone.utc)
            + timedelta(minutes=10)
        )

        await VerificationCodeRepository.create(
            db=db,
            user_id=user.id,
            code_hash=code_hash,
            expires_at=expires_at,
        )

        print("New verification code:", code)

        return {
            "message": "Verification code sent successfully"
        }