from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
from models.user import User
from schemas.user import UserCreate, UserResponse
from dependencies.auth import get_current_user
from utils.security import hash_password


router = APIRouter(prefix="/api/users", tags=["Users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db), limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0)):
    return db.query(User).offset(offset).limit(limit).all()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if db.query(User).filter((User.username == payload.username) | (User.email == payload.email)).first():
        raise HTTPException(status_code=400, detail="Nom d'utilisateur ou email déjà utilisé")
    new_user = User(username=payload.username, email=payload.email, password=hash_password(payload.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, payload: UserCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    # Basic unique checks
    existing = db.query(User).filter((User.username == payload.username) | (User.email == payload.email), User.id != user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur ou email déjà utilisé")

    user.username = payload.username
    user.email = payload.email
    user.password = hash_password(payload.password)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    db.delete(user)
    db.commit()
    return
