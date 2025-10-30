from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
from models.album import Album
from models.artist import Artist
from schemas.album import AlbumCreate, AlbumResponse, AlbumWithArtistResponse
from models.song import Song
from schemas.song import SongCreate, SongResponse


router = APIRouter(prefix="/api/albums", tags=["Albums"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _assert_artist_exists(db: Session, artist_id: int):
    if not db.query(Artist).filter(Artist.id == artist_id).first():
        raise HTTPException(status_code=404, detail="Artiste associé introuvable")


@router.get("/", response_model=List[AlbumWithArtistResponse])
def list_albums(db: Session = Depends(get_db), limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0)):
    albums = db.query(Album).offset(offset).limit(limit).all()
    results: list[AlbumWithArtistResponse] = []
    # Preload artists by ids to minimize queries
    artist_ids = {al.artist_id for al in albums}
    artists_map = {a.id: a.name for a in db.query(Artist).filter(Artist.id.in_(artist_ids)).all()} if artist_ids else {}
    for al in albums:
        results.append(
            AlbumWithArtistResponse(
                id=al.id,
                title=al.title,
                cover=al.cover,
                release_date=al.release_date,
                artist_id=al.artist_id,
                artist_name=artists_map.get(al.artist_id),
            )
        )
    return results


@router.get("/{album_id}", response_model=AlbumWithArtistResponse)
def get_album(album_id: int, db: Session = Depends(get_db)):
    album = db.query(Album).filter(Album.id == album_id).first()
    if not album:
        raise HTTPException(status_code=404, detail="Album introuvable")
    artist = db.query(Artist).filter(Artist.id == album.artist_id).first()
    return AlbumWithArtistResponse(
        id=album.id,
        title=album.title,
        cover=album.cover,
        release_date=album.release_date,
        artist_id=album.artist_id,
        artist_name=artist.name if artist else None,
    )


@router.post("/", response_model=AlbumResponse, status_code=status.HTTP_201_CREATED)
def create_album(payload: AlbumCreate, db: Session = Depends(get_db)):
    _assert_artist_exists(db, payload.artist_id)
    album = Album(**payload.dict())
    db.add(album)
    db.commit()
    db.refresh(album)
    return album


@router.put("/{album_id}", response_model=AlbumResponse)
def update_album(album_id: int, payload: AlbumCreate, db: Session = Depends(get_db)):
    album = db.query(Album).filter(Album.id == album_id).first()
    if not album:
        raise HTTPException(status_code=404, detail="Album introuvable")
    _assert_artist_exists(db, payload.artist_id)
    for k, v in payload.dict().items():
        setattr(album, k, v)
    db.commit()
    db.refresh(album)
    return album


@router.delete("/{album_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_album(album_id: int, db: Session = Depends(get_db)):
    album = db.query(Album).filter(Album.id == album_id).first()
    if not album:
        raise HTTPException(status_code=404, detail="Album introuvable")
    db.delete(album)
    db.commit()
    return


# Relations: songs of an album
@router.get("/{album_id}/songs", response_model=List[SongResponse])
def list_songs_of_album(album_id: int, db: Session = Depends(get_db), limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0)):
    album = db.query(Album).filter(Album.id == album_id).first()
    if not album:
        raise HTTPException(status_code=404, detail="Album introuvable")
    return db.query(Song).filter(Song.album_id == album_id).offset(offset).limit(limit).all()


@router.post("/{album_id}/songs", response_model=SongResponse, status_code=status.HTTP_201_CREATED)
def create_song_in_album(album_id: int, payload: SongCreate, db: Session = Depends(get_db)):
    album = db.query(Album).filter(Album.id == album_id).first()
    if not album:
        raise HTTPException(status_code=404, detail="Album introuvable")
    # enforce album_id
    data = payload.dict()
    data["album_id"] = album_id
    song = Song(**data)
    db.add(song)
    db.commit()
    db.refresh(song)
    return song
