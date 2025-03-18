from sqlalchemy import Column, String, Integer
from .database import Base

class User(Base):
    """Modelo da tabela de usuários no banco de dados."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(64), nullable=False)
