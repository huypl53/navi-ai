from app.model.baseMd import BaseMd
from app.model.masteryBktBaseMixin import MasteryBktBaseMixin


class MasteryBktMultiGsMd(MasteryBktBaseMixin, BaseMd):
    __tablename__ = 'mastery_bkt_multi_gs'
