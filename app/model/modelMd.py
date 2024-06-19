from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.sql import func

from app.model.relation import model_user_md
from app.model import BaseMd


class ModelMd(BaseMd):
    __tablename__ = "model"
    id = Column(Integer, primary_key=True)
    create_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime)
    saved_at = Column(String)  # relative path to model .pkl
    user_id = Column(String, ForeignKey("user.id"))

    # users = relationship("User", secondary=model_user_md,
    #                      back_populates="models")
