import hashlib
import datetime
import jwt
from sqlalchemy.orm import Session
from fastapi import HTTPException, Header
from models.usuario_model import User

SECRET_KEY = "secret123"

def create_token(username, email):
    """Gera um token JWT para autenticação."""
    payload = {
        "sub": username,
        "email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token: str = Header(None)):
    """Verifica a validade do token JWT."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

def register_user(db: Session, username: str, password: str):
    """Registra um novo usuário no banco de dados."""
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    db_user = User(username=username, password_hash=hashed_password)
    
    db.add(db_user)
    db.commit()
    return {"message": "Usuário cadastrado com sucesso!"}

def login(db: Session, username: str, password: str, email: str):
    """Realiza login verificando credenciais e retorna um token JWT."""
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    db_user = db.query(User).filter(User.username == username, User.password_hash == hashed_password).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Credenciais inválidas")

    token = create_token(username, email)
    return {"message": "Login bem-sucedido!", "token": token}
