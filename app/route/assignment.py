from fastapi import APIRouter
from app.repository import AssignmentRepo
from app.schema import AssignmentSch
from app.utils.logging import AppLogger
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db


logger = AppLogger().get_logger()

router = APIRouter(prefix="/v1/assignment")


_assign_repo = AssignmentRepo()


@router.post("/")
async def add_user(assignment: AssignmentSch, db_session: AsyncSession = Depends(get_db)):
    logger.info(f"Post assignment: {assignment}")
    return await _assign_repo.add_assginment(assignment, db_session)
    # await _user_repo.add_user(user.id, user.name)
