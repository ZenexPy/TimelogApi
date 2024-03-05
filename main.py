from fastapi import FastAPI
from src.projects.views import router as router_projects
from src.timelog.views import router as router_timelog
from src.users.views import auth_router





app = FastAPI()

app.include_router(router=router_projects)

app.include_router(router=router_timelog)

app.include_router(router=auth_router)




@app.get("/")
def index_hello():
    return {"message": 'Hello, world!'}
