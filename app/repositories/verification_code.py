from datetime import datetime, timezone

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.verification_code import VerificationCodeModel


class VerificationCodeRepository:

    @staticmethod
    async def create(
        db: AsyncSession,
        *,
        user_id: int,
        code_hash: str,
        expires_at: datetime,
    ) -> VerificationCodeModel:
        verification_code = VerificationCodeModel(
            user_id=user_id,
            code_hash=code_hash,
            expires_at=expires_at,
        )

        db.add(verification_code)

        await db.commit()
        await db.refresh(verification_code)

        return verification_code

    @staticmethod
    async def get_latest_valid(
        db: AsyncSession,
        user_id: int,
    ) -> VerificationCodeModel | None:
        now = datetime.now(timezone.utc)

        result = await db.execute(
            select(VerificationCodeModel)
            .where(
                VerificationCodeModel.user_id == user_id,
                VerificationCodeModel.used_at.is_(None),
                VerificationCodeModel.expires_at > now,
            )
            .order_by(
                VerificationCodeModel.created_at.desc()
            )
        )

        return result.scalars().first()

    @staticmethod
    async def mark_as_used(
        db: AsyncSession,
        verification_code: VerificationCodeModel,
    ) -> VerificationCodeModel:
        verification_code.used_at = datetime.now(timezone.utc)

        await db.commit()
        await db.refresh(verification_code)

        return verification_code

    @staticmethod
    async def get_latest_by_user(
        db: AsyncSession,
        user_id: int,
    ) -> VerificationCodeModel | None:
        result = await db.execute(
            select(VerificationCodeModel)
            .where(
                VerificationCodeModel.user_id == user_id
            )
            .order_by(
                VerificationCodeModel.created_at.desc()
            )
        )

        return result.scalars().first()

    @staticmethod
    async def invalidate_all_active(
        db: AsyncSession,
        user_id: int,
    ) -> None:
        await db.execute(
            update(VerificationCodeModel)
            .where(
                VerificationCodeModel.user_id == user_id,
                VerificationCodeModel.used_at.is_(None),
            )
            .values(
                used_at=datetime.now(timezone.utc)
            )
        )

        await db.commit()