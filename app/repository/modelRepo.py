from sqlalchemy.ext.asyncio import AsyncSession
from app.model.modelMd import ModelMd
from app.model.assignmentMd import AssignmentMd
from app.repository.baseRepo import BaseRepo
from app.repository.assignmentRepo import AssignmentRepo
from app.schema import AssignmentSch
from fastapi import Depends
import pandas as pd
from collections import defaultdict
from sqlalchemy.inspection import inspect

import datetime
from app.utils.logging import AppLogger
from app.db.connector import get_db, ses

logger = AppLogger().get_logger()


def query_to_dict(rset):
    result = defaultdict(list)
    for obj in rset:
        instance = inspect(obj)
        for key, x in instance.attrs.items():
            result[key].append(x.value)
    return result


class ModelRepo(BaseRepo):
    def __init__(self) -> None:
        self.assignmentRepo = AssignmentRepo()

    async def save_model(
        self, model_path: str, db_session: AsyncSession
    ):
        logger.info(f"DB is saving model at {model_path}")
        model: ModelMd = ModelMd(
            saved_at=model_path, modified_at=datetime.datetime.now()
        )
        await self.create(model, db_session)
        return model

    async def get_mastery(self, assignment: AssignmentSch, db_session: AsyncSession):
        assigns = await self.assignmentRepo.get_assigment_by_user(assignment.user_id, db_session)
        # print(f"get_mastery: {assigns.as_scalar()}")
        # results = pd.read_sql(db_session.query(AssignmentMd))
        results = pd.readsql
        # results = pd.read_sql_query(assigns.)
        print(f'padnas results: { results }')
