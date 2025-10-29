from pydantic import BaseModel
from typing import Optional

# 🔹 Modèle de base (champs communs)
class ArtistBase(BaseModel):
    name: str
    avatar: Optional[str] = None
    bio: Optional[str] = None

# 🔹 Pour la création (POST)
class ArtistCreate(ArtistBase):
    pass

# 🔹 Pour la réponse (GET)
class ArtistResponse(ArtistBase):
    id: int

    class Config:
        from_attributes = True  # Permet de convertir automatiquement les objets SQLAlchemy
