from fastapi import FastAPI
import uvicorn
from src.projects.views import router as router_projects

app = FastAPI()
app.include_router(router=router_projects)


@app.get("/")
def index_hello():
    return {"message": 'Hello, world!'}


# if __name__ == "main":
#     uvicorn.run("main:app", reload=True)
