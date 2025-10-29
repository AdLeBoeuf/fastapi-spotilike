from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from .associations import song_genres

class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    duration = Column(Float)
    artist_id = Column(Integer, ForeignKey("artists.id"))
    album_id = Column(Integer, ForeignKey("albums.id"))

    artist = relationship("Artist")
    album = relationship("Album", back_populates="songs")
    genres = relationship("Genre", secondary=song_genres, backref="songs")
