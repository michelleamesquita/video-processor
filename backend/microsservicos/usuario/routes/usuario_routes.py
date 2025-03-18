from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from models.database import get_db
from controllers.usuario_controller import register_user, login, verify_token
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str
    email: str

class RegisterRequest(BaseModel):
    username: str
    password: str

@router.post("/register/")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """Endpoint para registrar um novo usuário."""
    return register_user(db, request.username, request.password)

@router.post("/login/")
def user_login(request: LoginRequest, db: Session = Depends(get_db)):
    """Endpoint para realizar login e obter um token JWT."""
    return login(db, request.username, request.password, request.email)

@router.get("/protected/")
def protected_route(token: str = Header(None)):
    """Rota protegida que requer um token válido."""
    username = verify_token(token)
    return {"message": f"Bem-vindo, {username}! Esta é uma rota protegida."}
