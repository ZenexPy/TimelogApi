import pytest
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from fastapi.testclient import TestClient
from ..src.core.models.base import Base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from ..main import app
from ..src.core.db_init import db_init
from typing import AsyncGenerator
from sqlalchemy.pool import NullPool
from .settings import db_init_test

DATABASE_URL_TEST = f"postgresql+asyncpg://postgres_test:postgres_test@localhost:5433/postgres_test"

engine_test = create_async_engine(url=DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = async_sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[db_init.session_dependency] = override_get_async_session
app.dependency_overrides[db_init.get_scoped_session] = db_init_test.get_scoped_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


