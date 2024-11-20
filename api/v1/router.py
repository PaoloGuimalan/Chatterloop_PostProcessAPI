from fastapi import APIRouter
from api.v1.handlers import post_processing

router = APIRouter()

router.include_router(post_processing.post_processing_router, prefix="/post", tags=["post_processing"])