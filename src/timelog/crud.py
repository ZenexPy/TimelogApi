from datetime import datetime, timezone

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from .schemas import TimeLogCreate
from .dependencies import find_open_timelog

from ..core.models.timelog import TimeLog
from ..core.models.user import User


async def create_timelog(session: AsyncSession, create_model: TimeLogCreate, user: User) -> TimeLog:
    current_user_id = user.id

    open_timelog = await find_open_timelog(session=session, user=user)

    if open_timelog:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have an open TimeLog. Please close it before creating a new one."
        )
    
    timelog_data = create_model.model_dump(
        exclude_unset=True)
    timelog_data['user_fk'] = current_user_id
    timelog = TimeLog(**timelog_data)
    session.add(timelog)
    await session.commit()

    return timelog


async def close_timelog(session: AsyncSession, user: User):
    open_timelog = await find_open_timelog(session=session, user=user)

    if open_timelog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No open timelog found for the user"
        )

    open_timelog.end_time = datetime.now(timezone.utc)
    await session.commit()

    return open_timelog
