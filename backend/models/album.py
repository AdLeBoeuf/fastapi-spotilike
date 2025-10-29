from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    cover = Column(String(255))
    release_date = Column(Date)
    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False)

    artist = relationship("Artist", back_populates="albums")
    songs = relationship("Song", back_populates="album", cascade="all, delete")
