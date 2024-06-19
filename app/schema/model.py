from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Model(BaseModel):
    id: Optional[int]
    create_at: Optional[datetime]
    modified_at: Optional[datetime]
    # create_at: datetime = None
    # modified_at: datetime = None
    saved_at: Optional[str]
    user_id: Optional[int]
