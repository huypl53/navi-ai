from pydantic import BaseModel


class Assignment(BaseModel):
    order_id: int
    user_id: str
    correct: int  # -1: no response, 1: true, 0: false
    skill_name: str
    skill_id: int
    problem_id: int
    problem_name: str
    format_id: int
    assigment_id: int
