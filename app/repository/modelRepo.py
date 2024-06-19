from sqlalchemy.ext.asyncio import AsyncSession
from app.model.modelMd import ModelMd
from app.repository.baseRepo import BaseRepo
from fastapi import Depends

import datetime
from app.utils.logging import AppLogger
from app.db import get_db

logger = AppLogger().get_logger()


class ModelRepo(BaseRepo):
    # def __init__(self) -> None:
    #     pass

    async def create_model(
        self, model_path: str, db_session: AsyncSession = Depends(get_db)
    ):
        logger.info(f"DB is saving model at {model_path}")
        model: ModelMd = ModelMd(
            saved_at=model_path, modified_at=datetime.datetime.now()
        )
        await self.create(model, db_session)

    async def get_model_by_user_skill(
        user_id: str, skill_id: str, db_session: AsyncSession = Depends(get_db)
    ):
        return
