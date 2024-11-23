from fastapi import FastAPI
from api.v1 import router
from connections.mongo import MongoConnection
from services.v1.content_processing.ContentProcessingService import content_processing
from services.v1.image_processing.InputReaderService import input_reader
# from pydantic import BaseModel

app = FastAPI()

app.include_router(router.router, prefix='/v1')

MongoConnection.connect()
content_processing.load_model()
input_reader.load_model()

@app.get("/")
def default_root():
    return "Welcome to Chatterloop Post Process API!"