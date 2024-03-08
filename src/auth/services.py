from ..core.models.position import Position
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.db_init import db_init
from sqlalchemy import select, Result
from fastapi import Depends


async def check_position_id(session):
    stmt = select(Position).order_by(Position.id)
    result: Result = await session.execute(stmt)
    positions = result.scalars().all()
    positions_id = [position.id for position in positions]
    return positions_id