from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import Mapped, relationship, List, backref

from app.model.relation import model_user


class User:
    __tablename__ = "user"
    id = Column(String, primary_key=True)
    name = Column(String)
    # createAt = Column(DateTime)
    # modifiedAt = Column(DateTime)
    models = relationship("Model", secondary=model_user, back_populates="users")
