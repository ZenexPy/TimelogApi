from asyncio import current_task

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session


class DatabaseInit:

    def __init__(self) -> None:
        self.engine = create_async_engine(
            url=f"postgresql+asyncpg://postgres_test:postgres_test@localhost:5433/postgres_test",
            echo=True,
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self):
        session = self.get_scoped_session()
        yield session
        await session.close()


db_init_test = DatabaseInit()