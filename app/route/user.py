from fastapi import APIRouter
from app.repository import UserRepo
from app.schema import User
from app.utils.logging import AppLogger


logger = AppLogger().get_logger()

router = APIRouter(prefix="/v1/user")


_user_repo = UserRepo()


@router.post("/create-user")
async def add_user(user: User):
    logger.info(f"Post user: {user}")
    _user_repo.add_user(user.id, user.name)


# @router.post("/save-model")
# async def save_model_path(path: str):
#     logger.info(f"Save model path, got: {path}")
