from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    username: str  # ou email si tu préfères, on garde username ici
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
