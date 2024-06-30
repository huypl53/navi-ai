import asyncio
import datetime
from collections import defaultdict

import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.inspection import inspect

from app.model.assignmentMd import AssignmentMd
from app.model.bktParamsMd import BktParams
from app.repository.assignmentRepo import AssignmentRepo
from app.repository.baseRepo import BaseRepo
from app.schema import AssignmentSch, ModelSch
from app.utils.logging import AppLogger
from app.model.bktEnum import BKT_VARIANCES
from app.model.masteryBktBaseMixin import MasteryBktBaseMixin
from bkt.core import calc_pnl

logger = AppLogger().get_logger()


def query_to_dict(rset):
    result = defaultdict(list)
    for obj in rset:
        instance = inspect(obj)
        for key, x in instance.attrs.items():
            result[key].append(x.value)
    return result


class BktParamsRepo(BaseRepo):
    def __init__(self) -> None:
        self.assignmentRepo = AssignmentRepo()

    async def save_model(self, model: ModelSch, db_session: AsyncSession):
        logger.info(f"DB is saving model at {model}")
        model: BktParams = BktParams(
            user_id=model.user_id,
            saved_at=model.saved_at,
            modified_at=datetime.datetime.now(),
        )
        await self.create(model, db_session)
        return model

    async def get_mastery(self, assignment: AssignmentSch, db_session: AsyncSession):
        # TODO: saving assignment  task to new coroutine
        asyncio.create_task(
            self.assignmentRepo.add_assginment(assignment))

        bkt_params_md = await self.get_infer_model_by_skill(
            assignment.skill_id, db_session)
        if bkt_params_md is None:
            # TODO: no model available
            return {'error': 'No model available'}

        try:
            assert assignment.correct in [0, 1]
            m_pl, m_ps, m_pt, m_pg = bkt_params_md.ppl, bkt_params_md.ps, bkt_params_md.pt, bkt_params_md.pg
            BktUserVariance: MasteryBktBaseMixin = BKT_VARIANCES[bkt_params_md.model_type]
            bkt_user_variance = await self.get_user_mastery_bkt_variance(BktUserVariance, assignment.user_id, assignment.skill_id, db_session)

            if bkt_user_variance is None:
                # Use skill's P(L)
                pl = m_pl
            else:  # Use user's P(L) according to his skill
                pl = bkt_user_variance.pl

            mastery = calc_pnl(pl, m_ps, m_pt, m_pg, assignment.correct)
            result = {"mastery": mastery}
            logger.info(result)
            return result
        except Exception as e:
            # TODO: handle exception
            msg = {'error': str(e)}
            return msg

    async def get_user_mastery_bkt_variance(self, BktUserVariance: MasteryBktBaseMixin,  user_id: int, skill_id: int, db_session: AsyncSession) -> MasteryBktBaseMixin | None:
        stmt = select(BktUserVariance).where(
            BktUserVariance.user_id == user_id and BktUserVariance.skill_id == skill_id)
        results = await db_session.execute(stmt)
        result = results.first()
        return result[0] if result is not None else result

    async def get_infer_model_by_skill(self, skill_id: int, db_session: AsyncSession) -> BktParams | None:
        '''
        Return: designated model or None
        '''
        stmt = select(BktParams).where(
            BktParams.skill_id == skill_id).order_by(BktParams.active.desc())
        results = await db_session.execute(stmt)
        result = results.first()
        return result[0] if result is not None else result

    async def get_models_by_skill(self, skill_id: int, db_session: AsyncSession):
        stmt = select(BktParams).where(
            BktParams.skill_id).order_by(BktParams.active)
        results = await db_session.execute(stmt)
        return results

    async def get_models_by_user(self, user_id: str, db_session: AsyncSession):
        stmt = select(BktParams).where(BktParams.user_id == user_id)
        result = await db_session.execute(stmt)
        l = result.scalars().all()
        return l
