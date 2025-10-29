from sqlalchemy import Table, Column, Integer, ForeignKey
from database import Base


song_genres = Table(
    "song_genres",
    Base.metadata,
    Column("song_id", Integer, ForeignKey("songs.id", ondelete="CASCADE"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True),
)
