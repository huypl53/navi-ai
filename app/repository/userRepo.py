from app.repository.baseRepo import BaseRepo
from app.utils.logging import AppLogger
from sqlalchemy.ext.asyncio import AsyncSession
from app.model.userMd import UserMd
from app.schema import UserSch

logger = AppLogger().get_logger()


class UserRepo(BaseRepo):

    async def create_user(
        self, user: UserSch, db_session: AsyncSession
    ):
        logger.info(f"Create new user: {user}")
        record: UserMd = UserMd(id=user.id, name=user.name)
        await self.create(record, db_session)
        return record
