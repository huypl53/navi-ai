from typing import Dict
from app.model.masteryBktBaseMixin import MasteryBktBaseMixin
from app.model.masteryMultiGsMd import MasteryBktMultiGsMd
from app.model.masteryMultiLearnMd import MasteryBktMultiLearnMd
from app.model.masteryMultiPairMd import MasteryBktMultiPairMd
from app.model.masteryMultiPriorMd import MasteryBktMultiPriorMd

BKT_VARIANCES: Dict[int, MasteryBktBaseMixin] = {
    1: MasteryBktMultiGsMd,
    2: MasteryBktMultiLearnMd,
    3: MasteryBktMultiPairMd,
    4: MasteryBktMultiPriorMd
}
