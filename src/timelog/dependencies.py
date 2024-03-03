from fastapi import Path, Depends, HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import manager
from ..auth.jwt_auth import auth_backend
from ..core.models.user import User
from ..core.models.timelog import TimeLog

from fastapi_users import FastAPIUsers

def get_current_user():
    fastapi_users = FastAPIUsers[User, int](
        manager.get_user_manager,
        [auth_backend],
    )
    current_user = fastapi_users.current_user()
    return current_user


async def find_open_timelog(session: AsyncSession, user: User):
    open_timelog = await session.execute(
        select(TimeLog).where(
            and_(
                TimeLog.user_fk == user.id,
                TimeLog.end_time.is_(None)
            )
        ).order_by(TimeLog.start_time.desc()).limit(1)
    )
    return open_timelog.scalar_one_or_none()