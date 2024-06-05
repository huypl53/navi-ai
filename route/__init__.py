from fastapi import APIRouter, File, UploadFile

from model import NaviPredictor

router = APIRouter()
predictor = NaviPredictor()


@router.post("/get-mastery")
async def get_mastery():

    response = predictor.predict()

    return "yolo"
