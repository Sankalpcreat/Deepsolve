from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    caption = Column(String(255), nullable=True)
    post_media_url = Column(String(255), nullable=False) 
    background_music_url = Column(String(255), nullable=True)
    post_category = Column(String(50), nullable=True)
    datetime_posted = Column(DateTime, default=datetime.utcnow)

    
    publisher_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    
    publisher = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    

    def __repr__(self):
        return f"<Post id={self.id}, caption={self.caption}>"