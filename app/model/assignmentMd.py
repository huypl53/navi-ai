from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, Text
from app.model.baseMd import BaseMd


class AssignmentMd(BaseMd):
    __tablename__ = "assignment"
    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    correct = Column(Integer)
    skill_name = Column(String(512))
    skill_id = Column(Integer)
    problem_id = Column(Integer)
    problem_name = Column(String(512))
    format_id = Column(Integer)
    assigment_id = Column(Integer)
