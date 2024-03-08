# **TimeLog Api**

## Introduction

This API is a service that allows recording employees' work processes. It includes the following capabilities: recording the start of work, recording the end of work, the project being worked on, and, of course, the employee performing the work. At the moment, the API project is only a **basic** concept with authentication, login, and logout capabilities. Updates are possible in the future.

You can use this repository to obtain information for building your own API. A more detailed overview of what has been implemented so far will be provided next.



## Database connection

### Pydantic Settings Classs

This class is necessary for more convenient designation of settings for connecting to the database. We use "BaseSetting" from "pydantic_settings" as the inherited class. The key point here is the use of the "SettingsConfigDict" class to initialize the .env file for substituting variables into the URL for connecting to the database.

```
class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "secret" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "secret" / "jwt-public.pem"

class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    auth_jwt: AuthJWT = AuthJWT()

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def DATABASE_URL_psycopg(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
```
As you can see  we also use class AuthJWT for JWT denotion keys.

### Class DatabseInit

This class will serve as the primary tool for interacting with the database. As seen from the class, SQLAlchemy is used here.
```
class DatabaseInit:

    def __init__(self) -> None:
        self.engine = create_async_engine(
            url=settings.DATABASE_URL_asyncpg,
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
```
In the \_\_init\_\_ method, the database engine is initialized using the create_async_engine function. The database URL specified in the settings (settings.DATABASE_URL_asyncpg) is used, and SQL queries output is enabled (echo=True).

Then, a session factory (session_factory) is created using the async_sessionmaker function, which is bound to the created engine. Session parameters such as autoflush (autoflush=False), autocommit (autocommit=False), and expire on commit (expire_on_commit=False) are also configured here.

The get_scoped_session method returns a new session set in a specific context specified by the current_task function.

"session_dependency" is an asynchronous generator that creates a session using the get_scoped_session method, provides it within the working context, and automatically closes it upon completion of work.

## Usage

There are many ways to use this class as database connection util. Two of them looks like this:

```
@router.put("/{project_id}/")
async def update_product(
    project_update: ProjectUpdate,
    project = Depends(get_project_by_id),
    session: AsyncSession = Depends(db_init.session_dependency)
    ):
    return await crud.update_project(
        session=session,
        project=project,
        project_update=project_update
    )
```
As you can see, here we use the Depends function from FastAPI, passing in the session_dependency from the DatabaseInit class. In other words, we indicate that the session during request processing will depend specifically on this function.

Other way how to perform database connection looks like this:
```
session = db_init.get_scoped_session()
    positions_id = await check_position_id(session=session)
```
Here we create a session outside the Depends function. Please note that to avoid overloading the database connection pool, you need to close the session. You can do this by calling 'session.close()' or modify the DatabaseInit class according to your needs.

### Crud (Create, Read, Update, Delete)

You can easily find CRUD operations in the repository within the entity folders, for example: projects, timelog, user.

```
async def get_project_all(session: AsyncSession) -> list[Project_model]:
    stmt = select(Project_model).order_by(Project_model.id)
    result: Result = await session.execute(stmt)
    projects = result.scalars().all()
    return list(projects)
``` 
This function later you can use in your views.py for user interaction with endpoints

```
@router.get("/", response_model=list[ProjectGet])
async def get_projects(session: AsyncSession = Depends(db_init.session_dependency)):

    return await crud.get_project_all(session=session)
```

