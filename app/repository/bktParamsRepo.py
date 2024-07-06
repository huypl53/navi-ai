import asyncio
from datetime import datetime
from collections import defaultdict
from typing import Type

import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.inspection import inspect

from app.model.assignmentMd import AssignmentMd
from app.model.bktParamsMd import BktParamsMd
from app.repository.assignmentRepo import AssignmentRepo
from app.repository.baseRepo import BaseRepo
from app.schema import AssignmentSch, ModelSch
from app.utils.logging import AppLogger
from app.model.bktEnum import BKT_VARIANCES
from app.model.masteryBktBaseMixin import MasteryBktBaseMixin
from bkt.core import calc_pnl
from app.db import session_factory

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
        logger.warning(f"DB is saving model at {model}")
        model: BktParamsMd = BktParamsMd(
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

        try:
            assert assignment.correct in [0, 1]
            model_type = 2  # choose by default if there is no active model
            if bkt_params_md is None:
                # no model available
                m_pl, m_ps, m_pt, m_pg = 0.17345, 0.20771, 0.42647, 0.33938
                asyncio.create_task(self.create_bkt_params(
                    m_pl, m_ps, m_pt, m_pg, assignment.skill_id, active=2))
            else:
                m_pl, m_ps, m_pt, m_pg = bkt_params_md.ppl, bkt_params_md.ps, bkt_params_md.pt, bkt_params_md.pg
                model_type = bkt_params_md.model_type
            BktUserVariance: Type[MasteryBktBaseMixin] = BKT_VARIANCES[model_type]
            bkt_user_variance = await self.get_user_mastery_bkt_variance(BktUserVariance, assignment.user_id, assignment.skill_id, db_session)

            # Use skill's P(L)
            pl = m_pl
            if bkt_user_variance:
                pl = bkt_user_variance.pl

            mastery = calc_pnl(pl, m_ps, m_pt, m_pg, assignment.correct)
            logger.warning(f'bkt_user_variance: {bkt_user_variance}')
            if bkt_user_variance is None:
                asyncio.create_task(self.create_user_mastery_model(
                    BktUserVariance, assignment.user_id, assignment.skill_id, mastery))

            else:  # Use user's P(L) according to his skill
                bkt_user_variance.pl = mastery
                await self.update_user_mastery_model(
                    bkt_user_variance, db_session)

            result = {"mastery": mastery}
            logger.warning(result)
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

    async def get_infer_model_by_skill(self, skill_id: int, db_session: AsyncSession) -> BktParamsMd | None:
        '''
        Return: designated model or None
        '''
        stmt = select(BktParamsMd).where(
            BktParamsMd.skill_id == skill_id).order_by(BktParamsMd.active.desc())
        results = await db_session.execute(stmt)
        result = results.first()
        return result[0] if result is not None else result

    async def get_models_by_skill(self, skill_id: int, db_session: AsyncSession):
        stmt = select(BktParamsMd).where(
            BktParamsMd.skill_id).order_by(BktParamsMd.active)
        results = await db_session.execute(stmt)
        return results

    async def create_bkt_params(self, m_pl, m_ps, m_pt, m_pg, skill_id: int, active=2, db_session: AsyncSession = None):
        is_new_sess = True if not db_session else False
        if not db_session:
            db_session = session_factory()
        try:
            bkt_params_md = BktParamsMd()
            bkt_params_md.ppl, bkt_params_md.ps, bkt_params_md.pt, bkt_params_md.pg = m_pl, m_ps, m_pt, m_pg
            bkt_params_md.model_type = 2  # model to infer and experience
            bkt_params_md.create_at = datetime.now()
            bkt_params_md.modified_at = datetime.now()
            # active:  2 - used for inference and experiment; 1 - used for experiment only; -2, -1: not used anymore
            bkt_params_md.active = active
            bkt_params_md.skill_id = skill_id

            await self.create(bkt_params_md, db_session)

        except Exception as e:
            logger.error(
                f'{e}. Create bkt params {bkt_params_md.__dict__} failed!')
            return None
        finally:
            if is_new_sess:
                await db_session.close()

    async def create_user_mastery_model(self, BktUserVariance: Type[MasteryBktBaseMixin], user_id: int, skill_id: int, pl: float, db_session: AsyncSession = None):
        is_new_sess = True if not db_session else False
        if not db_session:
            db_session = session_factory()
        try:
            user_mastery_model = BktUserVariance()
            user_mastery_model.user_id = user_id
            user_mastery_model.skill_id = skill_id
            user_mastery_model.pl = pl
            user_mastery_model.updated_at = datetime.now()
            user_mastery_model.description = BktUserVariance.__name__
            await self.create(user_mastery_model, db_session)

        except Exception as e:
            logger.error(
                f'{e}. Create user_master_model* {user_mastery_model.__dict__} failed!')
        finally:
            if is_new_sess:
                await db_session.close()

    async def update_user_mastery_model(self, user_mastery_bkt: MasteryBktBaseMixin,  db_session: AsyncSession = None):
        is_new_sess = True if not db_session else False
        if not db_session:
            db_session = session_factory()
        try:
            await self.update(user_mastery_bkt, db_session)
        except Exception as e:
            logger.error(
                f'{e}. Update user_master_model* {user_mastery_bkt.__dict__} failed!')
        finally:
            if is_new_sess:
                await db_session.close()

    async def get_models_by_user(self, user_id: str, db_session: AsyncSession):
        stmt = select(BktParamsMd).where(BktParamsMd.user_id == user_id)
        result = await db_session.execute(stmt)
        l = result.scalars().all()
        return l
