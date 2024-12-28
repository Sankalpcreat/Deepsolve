from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    liked_on = Column(DateTime, default=datetime.utcnow)

    
    user = relationship("User", backref="likes")
    post = relationship("Post", backref="likes")

    def __repr__(self):
        return f"<Like id={self.id}, user_id={self.user_id}, post_id={self.post_id}>"