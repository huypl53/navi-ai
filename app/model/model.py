from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.model.relation import model_user


class Model:
    __tablename__ = "model"
    id = Column(String, primary_key=True)
    createAt = Column(DateTime)
    modifiedAt = Column(DateTime)
    savedAt = Column(String)  # relative path to model .pkl
    user_id = Column(String, ForeignKey("user.id"))

    users = relationship("User", secondary=model_user, back_populates="models")
