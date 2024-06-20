from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.model.modelMd import ModelMd
from app.model.assignmentMd import AssignmentMd
from app.repository.baseRepo import BaseRepo
from app.repository.assignmentRepo import AssignmentRepo
from app.schema import AssignmentSch
import pandas as pd
from collections import defaultdict
from sqlalchemy.inspection import inspect
from app.schema import ModelSch

import datetime
from app.utils.logging import AppLogger
from app.db.connector import get_db
from app.worker import NaviWorker
import asyncio

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
        self, model: ModelSch, db_session: AsyncSession
    ):
        logger.info(f"DB is saving model at {model}")
        model: ModelMd = ModelMd(
            user_id=model.user_id, saved_at=model.saved_at, modified_at=datetime.datetime.now()
        )
        await self.create(model, db_session)
        return model

    async def get_mastery(self, assignment: AssignmentSch, db_session: AsyncSession):
        # TODO: handle existed assignment
        asyncio.create_task(
            self.assignmentRepo.add_assginment(assignment, db_session))
        models = await self.get_models_by_user(assignment.user_id, db_session)
        model_paths = [m.saved_at for m in models]
        navi_worker = NaviWorker(model_paths)
        mastery = navi_worker.predict(assignment)
        print(f'mastery: {mastery}')
        return {'mastery': mastery}

    async def get_models_by_user(self, user_id: str, db_session: AsyncSession):
        stmt = select(ModelMd).where(ModelMd.user_id == user_id)
        result = await db_session.execute(stmt)
        print(result, )
        l = result.scalars().all()
        return l


def pandas_query_assigns(session, user_id: int):
    conn = session.connection()
    query = select(AssignmentMd).where(
        AssignmentMd.user_id == user_id)

    return pd.read_sql_query(query, conn)
