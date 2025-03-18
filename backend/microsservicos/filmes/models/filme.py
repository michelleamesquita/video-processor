from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class Filme(Base):
    __tablename__ = "filmes"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)

class FilmeCreate(BaseModel):
    titulo: str
    status: str
