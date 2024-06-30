from fastapi import APIRouter
from app.route.model import router as model_router
from app.route.assignment import router as assignment_router

router = APIRouter()


@router.get("/hello-world")
async def get_mastery():
    return "yolo"
