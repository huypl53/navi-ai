from app.model.baseMd import BaseMd
from app.model.masteryBktBaseMixin import MasteryBktBaseMixin


class MasteryBktMultiPriorMd(BaseMd, MasteryBktBaseMixin):
    __tablename__ = 'mastery_bkt_multi_prior'
