from fastapi import APIRouter, Request
from services.v1.image_processing.ImageProcessingService import ImageProcessingService

image_processing_router = APIRouter()

@image_processing_router.get("/")
def index():
    return "Image Processing Routes"

@image_processing_router.post("/generate_tag")
async def generate_tag(request: Request):
    payload = await request.json()
    referenceID = payload["referenceID"]
    referenceType = payload["referenceType"]

    image_data = await ImageProcessingService.fetch_image_src(referenceID, referenceType)

    return image_data