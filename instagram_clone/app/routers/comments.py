from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentRead
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

@router.post("/posts/{post_id}/comments", response_model=CommentRead)
def add_comment_to_post(
    post_id: int,
    comment_data: CommentCreate,
    token: str,
    db: Session = Depends(get_db)
):
    current_user = get_current_user(token, db)
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found.")

    new_comment = Comment(
        text=comment_data.text,
        user_id=current_user.id,
        post_id=post_id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.get("/posts/{post_id}/comments", response_model=List[CommentRead])
def get_comments_for_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found.")

    comments = db.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.datetime_commented.asc()).all()
    return comments