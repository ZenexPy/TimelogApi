from typing import Optional
from datetime import datetime

from fastapi_users import schemas
from pydantic import EmailStr, BaseModel
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic.version import VERSION as PYDANTIC_VERSION

from fastapi_users import models

PYDANTIC_V2 = PYDANTIC_VERSION.startswith("2.")

SCHEMA = TypeVar("SCHEMA", bound=BaseModel)

if PYDANTIC_V2:  # pragma: no cover

    def model_dump(model: BaseModel, *args, **kwargs) -> Dict[str, Any]:
        return model.model_dump(*args, **kwargs)  # type: ignore

    def model_validate(schema: Type[SCHEMA], obj: Any, *args, **kwargs) -> SCHEMA:
        return schema.model_validate(obj, *args, **kwargs)  # type: ignore

else:  # pragma: no cover  # type: ignore

    def model_dump(model: BaseModel, *args, **kwargs) -> Dict[str, Any]:
        return model.dict(*args, **kwargs)  # type: ignore

    def model_validate(schema: Type[SCHEMA], obj: Any, *args, **kwargs) -> SCHEMA:
        return schema.from_orm(obj)  # type: ignore


class UserRead(schemas.BaseUser[int]):
    id: int
    email: EmailStr
    username: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    position: str


class UserCreateCustom(schemas.CreateUpdateDictModel):
    email: EmailStr
    username: str
    password: str
    position_fk: int
    is_active: bool = True
    is_superuser: bool = True
    is_verified: bool = True

    def create_update_dict(self):
        return model_dump(
            self,
            exclude_unset=True,
            exclude={
                "id",
            },
        )

    def create_update_dict_superuser(self):
        return model_dump(self, exclude_unset=True, exclude={"id"})


class UserCreate(schemas.CreateUpdateDictModel):
    email: EmailStr
    username: str
    password: str
    position_fk: int

    class Config:
        orm_mode = True
        exclude_unset = True
        exclude = {"is_active", "is_superuser", "is_verified"}
