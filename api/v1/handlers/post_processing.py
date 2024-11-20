from fastapi import APIRouter, Request, Depends
from services.v1.image_processing.ImageProcessingService import ImageProcessingService
from services.v1.image_processing.ImageTagSyncingService import ImageTagSyncingService
from services.v1.content_processing.ContentProcessingService import ContentProcessingService
from api.v1.middlewares.jwtchecker import JWTChecker

post_processing_router = APIRouter()

@post_processing_router.get("/")
def index():
    return "Post Processing Routes"

@post_processing_router.post("/generate_tag", dependencies=[Depends(JWTChecker.check_user_token)])
async def generate_tag(request: Request):
    userID = request.state.userID;
    payload = await request.json()
    referenceID = payload["referenceID"]
    referenceType = payload["referenceType"]

    image_data = await ImageProcessingService.fetch_image_src(referenceID, referenceType)
    pre_prediction = await ImageProcessingService.handle_images_pre_prediction(image_data)
    await ImageTagSyncingService.save_tags_to_mongo(pre_prediction)

    content_processing = ContentProcessingService()
    content_processing.load_model()
    await content_processing.content_check(referenceID, referenceType)

    return pre_prediction