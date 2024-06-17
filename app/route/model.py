from fastapi import APIRouter
from app.schema import Assignment
from app.utils.logging import AppLogger

logger = AppLogger().get_logger()

router = APIRouter(prefix="/v1/model")


@router.post("/calc-mastery")
async def calc_mastery(assignment: Assignment):
    logger.info(f"Get assigment: {assignment}")


@router.post("/save-model")
async def save_model_path(path: str):
    logger.info(f"Save model path, got: {path}")
