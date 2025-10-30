from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import SessionLocal
from models.artist import Artist
from models.album import Album
from models.song import Song
from schemas.artist import ArtistCreate, ArtistResponse
from schemas.album import AlbumResponse
from schemas.song import SongResponse, SongWithAlbumResponse
from typing import List

router = APIRouter(prefix="/api/artists", tags=["Artists"])

# 🔹 Crée une session DB pour chaque requête
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🟢 GET - Liste de tous les artistes
@router.get("/", response_model=List[ArtistResponse])
def get_all_artists(db: Session = Depends(get_db), limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0)):
    return db.query(Artist).offset(offset).limit(limit).all()

# 🟢 GET - Détails d’un artiste par ID
@router.get("/{artist_id}", response_model=ArtistResponse)
def get_artist(artist_id: int, db: Session = Depends(get_db)):
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artist:
        raise HTTPException(status_code=404, detail="Artiste non trouvé")
    return artist

# 🟠 POST - Ajout d’un artiste
@router.post("/", response_model=ArtistResponse, status_code=status.HTTP_201_CREATED)
def create_artist(artist: ArtistCreate, db: Session = Depends(get_db)):
    new_artist = Artist(**artist.dict())
    db.add(new_artist)
    db.commit()
    db.refresh(new_artist)
    return new_artist

# 🔵 PUT - Modification d’un artiste
@router.put("/{artist_id}", response_model=ArtistResponse)
def update_artist(artist_id: int, updated_artist: ArtistCreate, db: Session = Depends(get_db)):
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artist:
        raise HTTPException(status_code=404, detail="Artiste non trouvé")

    for key, value in updated_artist.dict().items():
        setattr(artist, key, value)

    db.commit()
    db.refresh(artist)
    return artist

# 🔴 DELETE - Suppression d’un artiste
@router.delete("/{artist_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_artist(artist_id: int, db: Session = Depends(get_db)):
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artist:
        raise HTTPException(status_code=404, detail="Artiste non trouvé")

    db.delete(artist)
    db.commit()
    return


# Relations helpers
@router.get("/{artist_id}/albums", response_model=List[AlbumResponse])
def list_albums_for_artist(artist_id: int, db: Session = Depends(get_db), limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0)):
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artist:
        raise HTTPException(status_code=404, detail="Artiste non trouvé")
    return db.query(Album).filter(Album.artist_id == artist_id).offset(offset).limit(limit).all()


@router.get("/{artist_id}/songs", response_model=List[SongWithAlbumResponse])
def list_songs_for_artist(artist_id: int, db: Session = Depends(get_db), limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0)):
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artist:
        raise HTTPException(status_code=404, detail="Artiste non trouvé")

    # Join albums to get album titles alongside songs
    q = (
        db.query(Song, Album.title.label("album_title"))
        .outerjoin(Album, Song.album_id == Album.id)
        .filter(Song.artist_id == artist_id)
        .offset(offset)
        .limit(limit)
    )

    results = []
    for song, album_title in q.all():
        results.append(
            SongWithAlbumResponse(
                id=song.id,
                title=song.title,
                duration=song.duration,
                artist_id=song.artist_id,
                album_id=song.album_id,
                album_title=album_title,
            )
        )
    return results
