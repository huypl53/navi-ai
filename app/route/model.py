from fastapi import APIRouter
from app.repository import AssignmentRepo
from app.schema import AssignmentSch
from app.utils.logging import AppLogger
from app.repository import BktParamsRepo
from app.schema import ModelSch
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db

logger = AppLogger().get_logger()

router = APIRouter(prefix="/v1/model")

_model_repo = BktParamsRepo()
_assigment_repo = AssignmentRepo()


@router.post("/calc-mastery")
async def calc_mastery(
    assignment: AssignmentSch, db_session: AsyncSession = Depends(get_db)
):
    logger.info(f"Get assigment: {assignment}")

    # Write assigment to DB
    # assign = await _assigment_repo.add_assginment(assignment, db_session)
    # return result
    return await _model_repo.get_mastery(assignment, db_session)


from pydantic import BaseModel


class SessionPl(BaseModel):
    skill_id: int
    pl: float


@router.post("/update-skill-pl/")
async def update_session_pl(
    session_pl_update: SessionPl, db_session: AsyncSession = Depends(get_db)
):
    skill_id = session_pl_update.skill_id
    pl = session_pl_update.pl
    logger.info(f"Get skill id: {skill_id}")

    # Write assigment to DB
    # assign = await _assigment_repo.add_assginment(assignment, db_session)
    # return result
    return await _model_repo.update_skill_pl0(skill_id, pl, db_session)


@router.post("/save-model")
async def save_model_path(model: ModelSch, db_session: AsyncSession = Depends(get_db)):
    logger.info(f"Save model path, got: {model.saved_at}")
    return await _model_repo.save_model(model, db_session)
