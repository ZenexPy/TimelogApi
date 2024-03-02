from fastapi import FastAPI, Depends
import uvicorn
from src.projects.views import router as router_projects
from fastapi_users import FastAPIUsers

from src.auth import schemas, manager
from src.auth.jwt_auth import auth_backend
from src.core.models.user import User

app = FastAPI()

fastapi_users = FastAPIUsers[User, int](
    manager.get_user_manager,
    [auth_backend],
)

app.include_router(router=router_projects)

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

current_user = fastapi_users.current_user()

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"


@app.get("/")
def index_hello():
    return {"message": 'Hello, world!'}