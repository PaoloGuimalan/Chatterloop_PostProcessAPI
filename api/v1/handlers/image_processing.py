from fastapi import APIRouter

image_processing_router = APIRouter()

@image_processing_router.get("/")
def index():
    return "Tags Endpoint"