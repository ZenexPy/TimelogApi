from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from fastapi import HTTPException, status
from ..core.models.user import User
from .schemas import UserRead


async def get_users(session: AsyncSession, user: User) -> list[User]:
    if user.is_superuser != True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )
    stmt = select(User).options(joinedload(User.position)).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    users_with_positions = []
    for user in users:
        users_with_positions.append({
            "id": user.id,
            "email": user.email,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
            "is_verified": user.is_verified,
            "username": user.username,
            "position": user.position.title
        })
    return users_with_positions


async def get_user(user: User, session: AsyncSession) -> User | None:
    stmt = select(User).options(joinedload(User.position)).where(
        user.id == User.id).order_by(User.id)
    result: Result = await session.execute(stmt)
    user: User | None = result.scalar_one_or_none()
    if user is not None:
        return ({
            "id": user.id,
            "email": user.email,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
            "is_verified": user.is_verified,
            "username": user.username,
            "position": user.position.title
        })
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND
    )
