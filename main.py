from fastapi import FastAPI
from router import router

app =  FastAPI()

app.include_router(router)

@app.get("/")
def hello_world():
    return {"text": "Hello world"}