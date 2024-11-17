from fastapi import APIRouter
from api.v1.handlers import image_processing

router = APIRouter()

router.include_router(image_processing.image_processing_router, prefix="/image", tags=["image_processing"])