from fastapi import APIRouter
from app.repository import UserRepo
from app.schema import User
from app.utils.logging import AppLogger
from app.model import UserMd
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db


logger = AppLogger().get_logger()

router = APIRouter(prefix="/v1/user")


_user_repo = UserRepo()


@router.post("/create-user")
async def add_user(user: User, db_session: AsyncSession = Depends(get_db)):
    logger.info(f"Post user: {user}")
    return await _user_repo.create_user(user, db_session)
    # await _user_repo.add_user(user.id, user.name)
