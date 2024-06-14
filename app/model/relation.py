from sqlalchemy import Column, Integer, String, ForeignKey, Table
from model.base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship


"""
    each user is mapped to many model. Each model related to 
    one user is a variant of pyBKT model for that user
"""
model_user = Table(
    "model_user",
    Base.metadata,
    Column("model_id", String, ForeignKey("model.id")),
    Column("user_id", String, ForeignKey("user.id")),
)
