from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship

from app.model.relation import model_user_md


class UserMd:
    __tablename__ = "user"
    id = Column(String, primary_key=True)
    name = Column(String)
    # createAt = Column(DateTime)
    # modifiedAt = Column(DateTime)
    models = relationship("Model", secondary=model_user_md,
                          back_populates="users")
