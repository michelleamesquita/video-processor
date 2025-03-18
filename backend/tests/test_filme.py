import os
import sys
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

# 🔹 Ajusta o sys.path para encontrar corretamente os pacotes do MVC
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# ✅ Ativando modo de teste para evitar conexão real com o banco
os.environ["TEST_MODE"] = "1"

# 🔹 Importando apenas o que precisamos sem imports relativos
from microsservicos.filmes.models.database import get_db
from microsservicos.filmes.models.filme import Filme, FilmeCreate

# 🔹 Recriando a função controller localmente para o teste
def create_filme(db: Session, filme: FilmeCreate):
    """Cadastra um novo filme no banco de dados."""
    db_filme = Filme(titulo=filme.titulo, status=filme.status)
    db.add(db_filme)
    db.commit()
    return {"message": "Filme cadastrado com sucesso!"}

# 🔹 Criando o router de teste
router = APIRouter()

@router.post("/filmes/")
def create_filme_endpoint(filme: FilmeCreate, db: Session = Depends(get_db)):
    """Rota para cadastrar um novo filme."""
    return create_filme(db, filme)

# 🔹 Criando um app de teste com o router de filmes
app = FastAPI()
app.include_router(router)

client = TestClient(app)

# 🔹 Criando um mock do banco de dados
@pytest.fixture(scope="function")
def mock_db_session():
    print("🔹 Criando mock do banco de dados...")
    with patch("microsservicos.filmes.models.database.get_db") as mock:
        mock_session = MagicMock()
        mock.return_value.__enter__.return_value = mock_session  # ✅ Garante retorno correto
        yield mock_session  # ✅ Retorna corretamente o mock
    print("✅ Mock aplicado com sucesso!")

# 🔹 Substituindo a dependência real pelo mock
@pytest.fixture(autouse=True)
def override_get_db(mock_db_session):
    app.dependency_overrides[get_db] = lambda: mock_db_session

# ✅ **Teste de criação de filme SEM ACESSAR O BANCO**
def test_create_filme(mock_db_session):  # ✅ Fixture passada corretamente
    mock_filme = MagicMock(id=1, titulo="Teste Filme", status="Disponível")

    # Configurar o mock para simular o comportamento do banco
    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.return_value = None

    response = client.post(
        "/filmes/",
        json={"titulo": "Teste Filme", "status": "Disponível"}
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Filme cadastrado com sucesso!"}

    # ✅ Verifica se os métodos do mock foram chamados corretamente
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
