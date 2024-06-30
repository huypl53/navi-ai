from app.repository.baseRepo import BaseRepo
from app.utils.logging import AppLogger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.model import AssignmentMd
from app.schema import AssignmentSch
from app.db import get_db

logger = AppLogger().get_logger()


class AssignmentRepo(BaseRepo):

    async def add_assginment(
        self, assignment: AssignmentSch, db_session: AsyncSession = None
    ) -> AssignmentMd | None:
        if not db_session:
            db_session = await anext(get_db())
        try:
            record: AssignmentMd = AssignmentMd(
                order_id=assignment.order_id,
                user_id=assignment.user_id,
                correct=assignment.correct,
                skill_name=assignment.skill_name,
                skill_id=assignment.skill_id,
                problem_id=assignment.problem_id,
                problem_name=assignment.problem_name,
                format_id=assignment.format_id,
                assigment_id=assignment.assigment_id,
            )
            await self.create(record, db_session)
            return record
        except Exception as e:
            logger.error(f'{e}. Create assignment {record.__dict__} failed!')
            return None
