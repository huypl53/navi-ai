from typing import List
from pyBKT.models import Model

MODELS_CONFIG = {}

from app.utils.logging import AppLogger

logger = AppLogger().get_logger()


class NaviWorker:
    """
    Woker inits models that attached to user_id
    """

    def __init__(self, model_paths: List[str]) -> None:
        self.models = []
        for p in model_paths:
            try:
                model = Model(seed=25).load(p)
                self.models.append(model)
            except Exception as e:
                logger.error(f"Init model failed at {p}. Error: {e}")

        self._model_num = len(self.models)
        pass

    def predict(self):

        pass

    def save(self):
        pass
