from app.utils.logging import AppLogger
from typing import List
from pyBKT.models import Model
import pandas as pd
from app.schema import AssignmentSch

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

    def predict(self, data: AssignmentSch):
        data = data.model_dump()
        df_assign = pd.DataFrame([data])
        results = []
        for m in self.models:
            r = m.predict(data=df_assign)
            results.append(r)

        # cols: correct_predictions  state_predictions
        try:
            results = pd.concat(results)
            state_prediction = results.loc[:, 'state_predictions'].mean()

            logger.info(state_prediction)
            return state_prediction
        except Exception as e:
            logger.error(f'Predict assignment failed! {e}')
            return None

    def save(self):
        pass
