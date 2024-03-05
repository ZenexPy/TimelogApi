from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.authentication import CookieTransport, JWTStrategy
from fastapi_users.authentication import AuthenticationBackend,  JWTStrategy


from ..core.models.user import User
from ..core.db_init import db_init
from ..core.config import settings

#SECRET = '!q2W#e4R$t6Y^u8I&i0O'


def get_user_db(session: AsyncSession = Depends(db_init.session_dependency)):
    yield SQLAlchemyUserDatabase(session, User)


cookie_transport = CookieTransport(
    cookie_name='auth_cookie', cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.auth_jwt.private_key_path.read_text(), 
        lifetime_seconds=3600,
        algorithm="RS256",
        public_key=settings.auth_jwt.public_key_path.read_text(),
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
