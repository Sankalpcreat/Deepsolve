from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.post import Post
from app.models.like import Like
from app.models.follow import Follow
from app.models.user import User
from app.schemas.post import PostCreate, PostRead
from app.core.security import decode_access_token

router = APIRouter()

def get_current_user(token: str, db: Session) -> User:
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token.")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")
    return user

@router.post("/", response_model=PostRead)
def create_post(
    post_data: PostCreate,
    token: str,
    db: Session = Depends(get_db)
):
    current_user = get_current_user(token, db)
    new_post = Post(
        caption=post_data.caption,
        post_media_url=post_data.post_media_url,
        background_music_url=post_data.background_music_url,
        post_category=post_data.post_category,
        publisher_user_id=current_user.id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/", response_model=List[PostRead])
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).order_by(Post.datetime_posted.desc()).all()
    return posts

@router.get("/{post_id}", response_model=PostRead)
def get_post_by_id(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found.")
    return post

@router.post("/like/{post_id}")
def like_post(post_id: int, token: str, db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found.")
    
    existing_like = db.query(Like).filter(
        Like.user_id == current_user.id,
        Like.post_id == post_id
    ).first()
    if existing_like:
        raise HTTPException(status_code=400, detail="You have already liked this post.")

    new_like = Like(user_id=current_user.id, post_id=post_id)
    db.add(new_like)
    db.commit()
    return {"detail": "Post liked successfully."}

@router.get("/feed", response_model=List[PostRead])
def get_user_feed(
    token: str,
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    current_user = get_current_user(token, db)
    
    followed_ids = db.query(Follow.followed_id).filter(Follow.follower_id == current_user.id).subquery()
    
    query = db.query(Post).filter(Post.publisher_user_id.in_(followed_ids))
    total_posts = query.count()
    offset = (page - 1) * limit
    posts = query.order_by(Post.datetime_posted.desc()).offset(offset).limit(limit).all()
    
    return posts