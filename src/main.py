from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def index_hello():
    return {"message": 'Hello, world!'}

















if __name__ == "main":
    uvicorn.run("main:app", reload=True)
