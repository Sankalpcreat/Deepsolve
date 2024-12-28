from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    pass

class CommentRead(CommentBase):
    id: int
    user_id: int
    post_id: int
    datetime_commented: datetime

    class Config:
        orm_mode = True