from typing import Annotated
from fastapi import Path, HTTPException, status, Depends

from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession
from ..auth import manager
from ..auth.jwt_auth import auth_backend
from ..core.models.user import User
from ..core.db_init import db_init
from . import crud

fastapi_users = FastAPIUsers[User, int](
    manager.get_user_manager,
    [auth_backend],
)
current_user = fastapi_users.current_user()





