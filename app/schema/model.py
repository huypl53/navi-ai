from typing import Optional

from pydantic import BaseModel


class Model(BaseModel):

    id: Optional[int]
    create_at: Optional[str]
    modified_at: Optional[str]
    model_type: Optional[int]
    active: Optional[int]
    skill_id: Optional[int]
    ppl: Optional[float]
    ps: Optional[float]
    pt: Optional[float]
    pg: Optional[float]
