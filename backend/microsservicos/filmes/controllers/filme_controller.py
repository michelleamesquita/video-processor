from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.filme import Filme, FilmeCreate

def create_filme(db: Session, filme: FilmeCreate):
    """Cadastra um novo filme no banco de dados."""
    db_filme = Filme(titulo=filme.titulo, status=filme.status)
    db.add(db_filme)
    db.commit()
    return {"message": "Filme cadastrado com sucesso!"}
