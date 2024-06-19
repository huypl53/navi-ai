from sqlalchemy import select
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
from app.db.connector import get_db
from app.worker import NaviWorker

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
        # assigns = await self.assignmentRepo.get_assigment_by_user(assignment.user_id, db_session)

        assigns = await db_session.run_sync(lambda s: pandas_query_assigns(s, assignment.user_id))
        # print(f'padnas results: { assigns }, len: {len(assigns)}')
        # logger.info(f'padnas results: { assigns }')

        # assigns._append(assignment.model_dump())
        assigns.loc[len(assigns)] = assignment.model_dump()

        # print(
        #     f'appended padnas results: { assigns }, len: {len(assigns)}, type: {type(assigns)}')
        models = await self.get_models_by_user(assignment.user_id, db_session)
        model_paths = [m.saved_at for m in models]
        navi_worker = NaviWorker(model_paths)
        # print(f'Workers: {navi_worker.models}')
        results = navi_worker.predict(assigns)
        if results is None:
            return
        r = results.loc[results['order_id'] == assignment.order_id]
        print(f'mastery: {r}, {type(r)}')

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
