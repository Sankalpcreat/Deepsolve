from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    profile_picture_url = Column(String(255), nullable=True)
    bio = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    
    posts = relationship("Post", back_populates="publisher", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="commenter", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User id={self.id}, username={self.username}>"