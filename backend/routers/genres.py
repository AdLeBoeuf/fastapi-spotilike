from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
from models.genre import Genre
from schemas.genre import GenreCreate, GenreResponse


router = APIRouter(prefix="/api/genres", tags=["Genres"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[GenreResponse])
def list_genres(db: Session = Depends(get_db), limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0)):
    return db.query(Genre).offset(offset).limit(limit).all()


@router.get("/{genre_id}", response_model=GenreResponse)
def get_genre(genre_id: int, db: Session = Depends(get_db)):
    genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(status_code=404, detail="Genre introuvable")
    return genre


@router.post("/", response_model=GenreResponse, status_code=status.HTTP_201_CREATED)
def create_genre(payload: GenreCreate, db: Session = Depends(get_db)):
    genre = Genre(**payload.dict())
    db.add(genre)
    db.commit()
    db.refresh(genre)
    return genre


@router.put("/{genre_id}", response_model=GenreResponse)
def update_genre(genre_id: int, payload: GenreCreate, db: Session = Depends(get_db)):
    genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(status_code=404, detail="Genre introuvable")
    for k, v in payload.dict().items():
        setattr(genre, k, v)
    db.commit()
    db.refresh(genre)
    return genre


@router.delete("/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(status_code=404, detail="Genre introuvable")
    db.delete(genre)
    db.commit()
    return
