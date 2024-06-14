from pydantic import BaseModel


class Assignment(BaseModel):
    userId: str
