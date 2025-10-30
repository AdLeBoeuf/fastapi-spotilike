from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from models import artist, album, song, genre, user
from routers import artists, albums, songs, genres, users
from routers import simple_auth

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Spotilike API",
    description="API REST pour la gestion des artistes, albums, morceaux et utilisateurs (projet Spotilike)",
    version="1.0.0"
)

# CORS (adapter le frontend origin si besoin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:4200",
        "http://127.0.0.1:4200",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(artists.router)
app.include_router(albums.router)
app.include_router(songs.router)
app.include_router(genres.router)
app.include_router(users.router)
app.include_router(simple_auth.router)

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API Spotilike 🚀"}


@app.get("/health")
def health():
    return {"status": "ok"}
