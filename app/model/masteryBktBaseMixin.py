from sqlalchemy import DateTime, Integer, Float, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class MasteryBktBaseMixin(object):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    skill_id: Mapped[int] = mapped_column(Integer)
    pl: Mapped[float] = mapped_column(Float)
    updated_at: Mapped[str] = mapped_column(DateTime, onupdate=datetime.now())
    description: Mapped[str] = mapped_column(Text)
    UniqueConstraint("user_id", "skill_id", name="unix_user_skill")
