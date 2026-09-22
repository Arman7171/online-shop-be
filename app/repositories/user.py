from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserModel


class UserRepository:

    @staticmethod
    async def get_by_email(
        db: AsyncSession,
        email: str,
    ) -> UserModel | None:
        result = await db.execute(
            select(UserModel).where(
                UserModel.email == email
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def create(
        db: AsyncSession,
        *,
        email: str,
        password_hash: str,
        first_name: str | None,
        last_name: str | None,
    ) -> UserModel:
        user = UserModel(
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
        )

        db.add(user)

        await db.commit()
        await db.refresh(user)

        return user

    @staticmethod
    async def mark_as_verified(
        db: AsyncSession,
        user: UserModel,
    ) -> UserModel:
        user.is_verified = True

        await db.commit()
        await db.refresh(user)

        return user