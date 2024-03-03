from fastapi import APIRouter, HTTPException, status, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from ..core.models.user import User
from .schemas import TimeLogGet, TimeLogCreate
from ..core.db_init import db_init
from .dependencies import get_current_user

router = APIRouter(tags=["Timelog"], prefix="/timelog")



@router.post("/", response_model=TimeLogGet, status_code=status.HTTP_201_CREATED)
async def create_timelog(create_model: TimeLogCreate, user: User = Depends(get_current_user()), session: AsyncSession = Depends(db_init.session_dependency)):
    return await crud.create_timelog(session=session, create_model=create_model, user=user)

@router.post("/close", response_model=TimeLogGet, status_code=status.HTTP_200_OK)
async def close_timelog(session: AsyncSession = Depends(db_init.session_dependency), user: User = Depends(get_current_user())):
    return await crud.close_timelog(session=session, user=user)















# @app.get("/protected-route")
# def protected_route(user: User = Depends(current_user)):
#     return f"Hello, {user.email}"