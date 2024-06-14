from fastapi import APIRouter, File, UploadFile

from worker import NaviWorker

router = APIRouter()
predictor = NaviWorker()


@router.post("/get-mastery")
async def get_mastery():

    response = predictor.predict()

    return "yolo"
