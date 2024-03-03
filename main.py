from fastapi import FastAPI, Depends
import uvicorn
from src.projects.views import router as router_projects
from src.timelog.views import router as router_timelog
from fastapi_users import FastAPIUsers

from src.auth import schemas, manager
from src.auth.jwt_auth import auth_backend
from src.core.models.user import User
fastapi_users = FastAPIUsers[User, int](
    manager.get_user_manager,
    [auth_backend],
)


app = FastAPI()

app.include_router(router=router_projects)

app.include_router(router=router_timelog)

app.include_router(
    fastapi_users.get_register_router(schemas.UserRead, schemas.UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)


@app.get("/")
def index_hello():
    return {"message": 'Hello, world!'}
