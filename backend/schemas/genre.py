from pydantic import BaseModel
from typing import Optional


class GenreBase(BaseModel):
    title: str
    description: Optional[str] = None


class GenreCreate(GenreBase):
    pass


class GenreResponse(GenreBase):
    id: int

    class Config:
        from_attributes = True
