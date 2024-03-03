from typing import Optional
from datetime import datetime

from fastapi_users import schemas
from pydantic import EmailStr


class UserRead(schemas.BaseUser[int]):
    id: int
    email: EmailStr
    username: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    position_fk: int


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    username: str
    registered_at: datetime
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    position_fk: int
