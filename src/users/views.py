from src.auth import manager
from src.users import schemas
from src.auth.jwt_auth import auth_backend
from .schemas import UserRead
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.db_init import db_init
from ..core.models.user import User

from fastapi import APIRouter, Depends
from .dependencies import fastapi_users, current_user
from . import crud

auth_router = APIRouter(tags=["User"], prefix="/users")

auth_router.include_router(
    fastapi_users.get_register_router(
        schemas.UserRead, schemas.UserCreate)
)

auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend)
)


@auth_router.get("/", response_model=list[UserRead])
async def get_all_users(session: AsyncSession = Depends(db_init.session_dependency),
                        user: User = Depends(current_user)):
    return await crud.get_users(session=session, user=user)


@auth_router.get("/{user_id}/", response_model=UserRead)
async def get_authorized_user(session: AsyncSession = Depends(db_init.session_dependency), user: User = Depends(current_user)):
    return await crud.get_user(session=session, user=user)
