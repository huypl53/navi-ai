from app.utils.logging import AppLogger
from typing import List
from pyBKT.models import Model
import pandas as pd

MODELS_CONFIG = {}


logger = AppLogger().get_logger()


class NaviWorker:
    """
    Woker inits models that attached to user_id
    """

    def __init__(self, model_paths: List[str]) -> None:
        self.models: List[Model] = []
        print(f'Paths: {model_paths}')
        for p in model_paths:
            try:
                model = Model(seed=25)
                model.load(p)
                self.models.append(model)
            except Exception as e:
                print(f"Init model failed at {p}. Error: {e}")
                logger.error(f"Init model failed at {p}. Error: {e}")

        self._model_num = len(self.models)

    def predict(self, data: pd.DataFrame):
        results = []
        for m in self.models:
            r = m.predict(data=data)
            results.append()
        if not len(results):
            return None
        return results
        # corrects = [ for r in results]
        # mastery_states = []

    def save(self):
        pass
