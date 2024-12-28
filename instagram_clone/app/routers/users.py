from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user import UserRead
from app.database import get_db
from app.models.user import User
from app.models.follow import Follow
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

@router.get("/profile/{user_id}", response_model=UserRead)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

@router.post("/follow/{user_id}")
def follow_user(
    user_id: int,
    token: str,
    db: Session = Depends(get_db)
):
    current_user = get_current_user(token, db)
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="You cannot follow yourself.")

    existing_follow = db.query(Follow).filter(
        Follow.follower_id == current_user.id,
        Follow.followed_id == user_id
    ).first()
    if existing_follow:
        raise HTTPException(status_code=400, detail="Already following this user.")

    new_follow = Follow(follower_id=current_user.id, followed_id=user_id)
    db.add(new_follow)
    db.commit()
    db.refresh(new_follow)
    return {"detail": "Followed user successfully."}

@router.delete("/unfollow/{user_id}")
def unfollow_user(
    user_id: int,
    token: str,
    db: Session = Depends(get_db)
):
    current_user = get_current_user(token, db)
    follow_record = db.query(Follow).filter(
        Follow.follower_id == current_user.id,
        Follow.followed_id == user_id
    ).first()
    if not follow_record:
        raise HTTPException(status_code=400, detail="Not following this user.")

    db.delete(follow_record)
    db.commit()
    return {"detail": "Unfollowed user successfully."}