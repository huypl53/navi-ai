from sqlalchemy import DateTime, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.model import BaseMd


class BktParams(BaseMd):
    __tablename__ = "bkt_params"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    create_at: Mapped[str] = mapped_column(DateTime, server_default=func.now())
    modified_at: Mapped[str] = mapped_column(
        DateTime)
    model_type: Mapped[int] = mapped_column(Integer)
    # active:  2 - used for inference and experiment; 1 - used for experiment only; -2, -1: not used anymore
    active: Mapped[int] = mapped_column(Integer)
    skill_id: Mapped[int] = mapped_column(Integer)
    ppl: Mapped[float] = mapped_column(Float)  # previous P(L)
    ps: Mapped[float] = mapped_column(Float)
    pt: Mapped[float] = mapped_column(Float)
    pg: Mapped[float] = mapped_column(Float)
