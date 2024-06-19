from app.repository.baseRepo import BaseRepo
from app.utils.logging import AppLogger
from sqlalchemy.ext.asyncio import AsyncSession
from app.model.userMd import UserMd
from app.schema import User

logger = AppLogger().get_logger()


class UserRepo(BaseRepo):

    async def create_user(
        self, user: User, db_session: AsyncSession
    ):
        logger.info(f"Create new user: {user}")
        model: UserMd = UserMd(id=user.id, name=user.name)
        await self.create(model, db_session)
        return model
