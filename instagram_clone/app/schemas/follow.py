from pydantic import BaseModel
from datetime import datetime

class FollowBase(BaseModel):
    pass

class FollowCreate(FollowBase):
    follower_id: int
    followed_id: int

class FollowRead(FollowBase):
    id: int
    follower_id: int
    followed_id: int
    followed_on: datetime

    class Config:
        orm_mode = True