from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..models.database import get_db
from ..controllers.filme_controller import create_filme
from ..models.filme import FilmeCreate

router = APIRouter()

@router.post("/filmes/")
def create_filme_endpoint(filme: FilmeCreate, db: Session = Depends(get_db)):
    """Rota para cadastrar um novo filme."""
    return create_filme(db, filme)
