from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
from models.song import Song
from models.artist import Artist
from models.album import Album
from schemas.song import SongCreate, SongResponse, SongWithNamesResponse
from models.genre import Genre
 


router = APIRouter(prefix="/api/songs", tags=["Songs"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _assert_fk_exists(db: Session, artist_id: int | None, album_id: int | None):
    if artist_id is not None and not db.query(Artist).filter(Artist.id == artist_id).first():
        raise HTTPException(status_code=404, detail="Artiste associé introuvable")
    if album_id is not None and not db.query(Album).filter(Album.id == album_id).first():
        raise HTTPException(status_code=404, detail="Album associé introuvable")


@router.get("/", response_model=List[SongWithNamesResponse])
def list_songs(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    q: str | None = Query(None, description="Search text in song title"),
    artist_id: int | None = Query(None),
    album_id: int | None = Query(None),
    genre_id: int | None = Query(None),
):
    query = (
        db.query(Song, Artist.name.label("artist_name"), Album.title.label("album_title"))
        .outerjoin(Artist, Song.artist_id == Artist.id)
        .outerjoin(Album, Song.album_id == Album.id)
    )

    if q:
        query = query.filter(Song.title.ilike(f"%{q}%"))
    if artist_id is not None:
        query = query.filter(Song.artist_id == artist_id)
    if album_id is not None:
        query = query.filter(Song.album_id == album_id)
    if genre_id is not None:
        # filter via relationship without explicit join
        query = query.filter(Song.genres.any(Genre.id == genre_id))

    query = query.offset(offset).limit(limit)
    results: list[SongWithNamesResponse] = []
    for song, artist_name, album_title in query.all():
        results.append(
            SongWithNamesResponse(
                id=song.id,
                title=song.title,
                duration=song.duration,
                artist_id=song.artist_id,
                artist_name=artist_name,
                album_id=song.album_id,
                album_title=album_title,
            )
        )
    return results


@router.get("/{song_id}", response_model=SongResponse)
def get_song(song_id: int, db: Session = Depends(get_db)):
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Morceau introuvable")
    return song


@router.post("/", response_model=SongResponse, status_code=status.HTTP_201_CREATED)
def create_song(payload: SongCreate, db: Session = Depends(get_db)):
    _assert_fk_exists(db, payload.artist_id, payload.album_id)
    song = Song(**payload.dict())
    db.add(song)
    db.commit()
    db.refresh(song)
    return song


@router.put("/{song_id}", response_model=SongResponse)
def update_song(song_id: int, payload: SongCreate, db: Session = Depends(get_db)):
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Morceau introuvable")
    _assert_fk_exists(db, payload.artist_id, payload.album_id)
    for k, v in payload.dict().items():
        setattr(song, k, v)
    db.commit()
    db.refresh(song)
    return song


@router.delete("/{song_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_song(song_id: int, db: Session = Depends(get_db)):
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Morceau introuvable")
    db.delete(song)
    db.commit()
    return


# Helpers routes for relations
@router.get("/by-artist/{artist_id}", response_model=List[SongWithNamesResponse])
def list_songs_by_artist(artist_id: int, db: Session = Depends(get_db), limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0)):
    if not db.query(Artist).filter(Artist.id == artist_id).first():
        raise HTTPException(status_code=404, detail="Artiste introuvable")
    q = (
        db.query(Song, Artist.name.label("artist_name"), Album.title.label("album_title"))
        .outerjoin(Artist, Song.artist_id == Artist.id)
        .outerjoin(Album, Song.album_id == Album.id)
        .filter(Song.artist_id == artist_id)
        .offset(offset)
        .limit(limit)
    )
    return [
        SongWithNamesResponse(
            id=s.id,
            title=s.title,
            duration=s.duration,
            artist_id=s.artist_id,
            artist_name=an,
            album_id=s.album_id,
            album_title=aln,
        )
        for (s, an, aln) in q.all()
    ]


@router.get("/by-album/{album_id}", response_model=List[SongWithNamesResponse])
def list_songs_by_album(album_id: int, db: Session = Depends(get_db), limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0)):
    if not db.query(Album).filter(Album.id == album_id).first():
        raise HTTPException(status_code=404, detail="Album introuvable")
    q = (
        db.query(Song, Artist.name.label("artist_name"), Album.title.label("album_title"))
        .outerjoin(Artist, Song.artist_id == Artist.id)
        .outerjoin(Album, Song.album_id == Album.id)
        .filter(Song.album_id == album_id)
        .offset(offset)
        .limit(limit)
    )
    return [
        SongWithNamesResponse(
            id=s.id,
            title=s.title,
            duration=s.duration,
            artist_id=s.artist_id,
            artist_name=an,
            album_id=s.album_id,
            album_title=aln,
        )
        for (s, an, aln) in q.all()
    ]


# Genre linking endpoints
@router.post("/{song_id}/genres/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
def add_genre_to_song(song_id: int, genre_id: int, db: Session = Depends(get_db)):
    song = db.query(Song).filter(Song.id == song_id).first()
    genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if not song or not genre:
        raise HTTPException(status_code=404, detail="Song ou Genre introuvable")
    if genre not in song.genres:
        song.genres.append(genre)
        db.commit()
    return


@router.delete("/{song_id}/genres/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_genre_from_song(song_id: int, genre_id: int, db: Session = Depends(get_db)):
    song = db.query(Song).filter(Song.id == song_id).first()
    genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if not song or not genre:
        raise HTTPException(status_code=404, detail="Song ou Genre introuvable")
    if genre in song.genres:
        song.genres.remove(genre)
        db.commit()
    return


@router.get("/{song_id}/genres", response_model=List[str])
def list_genres_of_song(song_id: int, db: Session = Depends(get_db)):
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Morceau introuvable")
    return [g.title for g in song.genres]
