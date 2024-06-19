from pydantic import BaseModel
from datetime import datetime


class Model(BaseModel):
    id: int
    create_at: datetime
    modified_at: datetime
    saved_at: str
    user_id: int
