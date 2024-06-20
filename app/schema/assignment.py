from typing import Optional
from pydantic import BaseModel


class Assignment(BaseModel):
    order_id: Optional[int]
    user_id: int
    correct: int  # -1: no response, 1: true, 0: false
    skill_name: str
    skill_id: int
    problem_id: int
    problem_name: str
    format_id: int
    assigment_id: int
