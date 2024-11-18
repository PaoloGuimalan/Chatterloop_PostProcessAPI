from fastapi import APIRouter, Request, Depends
from services.v1.image_processing.ImageProcessingService import ImageProcessingService
from api.v1.middlewares.jwtchecker import JWTChecker

image_processing_router = APIRouter()

@image_processing_router.get("/")
def index():
    return "Image Processing Routes"

@image_processing_router.post("/generate_tag", dependencies=[Depends(JWTChecker.check_user_token)])
async def generate_tag(request: Request):
    userID = request.state.userID;
    payload = await request.json()
    referenceID = payload["referenceID"]
    referenceType = payload["referenceType"]

    image_data = await ImageProcessingService.fetch_image_src(referenceID, referenceType)
    pre_prediction = await ImageProcessingService.handle_images_pre_prediction(image_data)

    return pre_prediction