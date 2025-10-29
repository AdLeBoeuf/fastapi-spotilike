from pydantic import BaseModel
from typing import Optional


class SongBase(BaseModel):
    title: str
    duration: Optional[float] = None
    artist_id: Optional[int] = None
    album_id: Optional[int] = None


class SongCreate(SongBase):
    pass


class SongResponse(SongBase):
    id: int

    class Config:
        from_attributes = True


class SongWithAlbumResponse(BaseModel):
    id: int
    title: str
    duration: Optional[float] = None
    artist_id: Optional[int] = None
    album_id: Optional[int] = None
    album_title: Optional[str] = None

    class Config:
        from_attributes = True


class SongWithNamesResponse(BaseModel):
    id: int
    title: str
    duration: Optional[float] = None
    artist_id: Optional[int] = None
    artist_name: Optional[str] = None
    album_id: Optional[int] = None
    album_title: Optional[str] = None

    class Config:
        from_attributes = True
