from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    caption: Optional[str] = None
    post_media_url: HttpUrl
    background_music_url: Optional[HttpUrl] = None
    post_category: Optional[str] = None

class PostCreate(PostBase):
    pass

class PostRead(PostBase):
    id: int
    datetime_posted: datetime
    publisher_user_id: int

    class Config:
        orm_mode = True