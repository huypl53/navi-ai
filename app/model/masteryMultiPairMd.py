from app.model.baseMd import BaseMd
from app.model.masteryBktBaseMixin import MasteryBktBaseMixin


class MasteryBktMultiPairMd(MasteryBktBaseMixin, BaseMd):
    __tablename__ = 'mastery_bkt_multi_pair'
