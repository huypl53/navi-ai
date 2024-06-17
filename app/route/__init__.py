from fastapi import APIRouter, File, UploadFile
from app.route.model import router as model_router
from app.route.user import router as user_router

router = APIRouter()


@router.get("/hello-world")
async def get_mastery():
    return "yolo"
