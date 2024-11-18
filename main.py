from fastapi import FastAPI
from api.v1 import router
from connections.mongo import MongoConnection
# from pydantic import BaseModel

app = FastAPI()

app.include_router(router.router, prefix='/v1')

MongoConnection.connect()

@app.get("/")
def default_root():
    return "Welcome to Chatterloop Post Process API!"