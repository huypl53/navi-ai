from app.repository.baseRepo import BaseRepo
from app.utils.logging import AppLogger
from sqlalchemy.ext.asyncio import AsyncSession
from app.model.userMd import UserMd
from app.db import get_db
from fastapi import Depends

logger = AppLogger().get_logger()


class AssignmentRepo(BaseRepo):
    # def __init__(self) -> None:
    #     pass

    async def add_assginment(
        self, id: str, name: str, db_session: AsyncSession = Depends(get_db)
    ):
        pass
