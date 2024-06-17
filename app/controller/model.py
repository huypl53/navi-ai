from app.model.modelMd import ModelMd
from app.repository.modelRepo import ModelRepo
from app.schema.assignment import Assignment
from app.worker.navi import NaviWorker
from operator import itemgetter
from app.utils.logging import AppLogger

logger = AppLogger().get_logger()


class ModelController:
    def __init__(self) -> None:
        self.modelRepo = ModelRepo(ModelMd)
        pass

    def predict_mastery(self, assignment: Assignment):

        logger.info(f"{self.__class__} predict_mastery got assignment: {assignment}")
        user_id = assignment.user_id
        skill_id = assignment.skill_id
        self.modelRepo.get_model_by_user_skill(user_id, skill_id)
        self.modelWorker = NaviWorker()
