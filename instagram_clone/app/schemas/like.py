from pydantic import BaseModel
from datetime import datetime

class LikeBase(BaseModel):
    pass

class LikeCreate(LikeBase):
    user_id: int
    post_id: int

class LikeRead(LikeBase):
    id: int
    user_id: int
    post_id: int
    liked_on: datetime

    class Config:
        orm_mode = True