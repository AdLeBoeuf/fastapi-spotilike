from pydantic import BaseModel
from typing import Optional
from datetime import date


class AlbumBase(BaseModel):
    title: str
    cover: Optional[str] = None
    release_date: Optional[date] = None
    artist_id: int


class AlbumCreate(AlbumBase):
    pass


class AlbumResponse(AlbumBase):
    id: int

    class Config:
        from_attributes = True


class AlbumWithArtistResponse(BaseModel):
    id: int
    title: str
    cover: Optional[str] = None
    release_date: Optional[date] = None
    artist_id: int
    artist_name: Optional[str] = None

    class Config:
        from_attributes = True
