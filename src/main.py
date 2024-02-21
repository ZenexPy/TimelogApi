from fastapi import FastAPI
import uvicorn
from products import router as router_products

app = FastAPI()
app.include_router(router=router_products)


@app.get("/")
def index_hello():
    return {"message": 'Hello, world!'}


if __name__ == "main":
    uvicorn.run("main:app", reload=True)
