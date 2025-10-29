from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import SessionLocal
from models.user import User
from schemas.auth import SignupRequest, TokenResponse
from utils.security import hash_password, verify_password, create_access_token


router = APIRouter(prefix="/api/auth", tags=["Auth"])
alias_router = APIRouter(prefix="/api/users", tags=["Auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    if db.query(User).filter((User.username == payload.username) | (User.email == payload.email)).first():
        raise HTTPException(status_code=400, detail="Nom d'utilisateur ou email déjà utilisé")

    user = User(username=payload.username, email=payload.email, password=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form.username).first()
    if not user or not verify_password(form.password, user.password):
        raise HTTPException(status_code=400, detail="Identifiants invalides")

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token)


# Aliases to match requested spec (/api/users/*)
@alias_router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def signup_alias(payload: SignupRequest, db: Session = Depends(get_db)):
    return signup(payload, db)


@alias_router.post("/login", response_model=TokenResponse)
def login_alias(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return login(form, db)
