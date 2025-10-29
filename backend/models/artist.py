from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from database import Base

class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    avatar = Column(String(255))
    bio = Column(Text)

    albums = relationship("Album", back_populates="artist", cascade="all, delete")
