from typing import List
from sqlalchemy.orm import Session
from app.models.post import Post
from app.models.follow import Follow

def generate_user_feed(user_id: int, db: Session, limit: int = 10, offset: int = 0) -> List[Post]:
    followed_ids_subquery = db.query(Follow.followed_id).filter(Follow.follower_id == user_id).subquery()
    query = db.query(Post).filter(Post.publisher_user_id.in_(followed_ids_subquery))
    return query.order_by(Post.datetime_posted.desc()).offset(offset).limit(limit).all()

def format_date(date):
    return date.strftime("%Y-%m-%d %H:%M:%S")