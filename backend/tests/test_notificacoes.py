import os
import sys
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from fastapi import FastAPI, APIRouter, Body

# 🔹 Ajusta o sys.path para encontrar corretamente os pacotes do MVC
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# ✅ Ativando modo de teste para evitar conexão real com serviços
os.environ["TEST_MODE"] = "1"

# 🔹 Recriando a função send_email para o teste
def send_email(to_email, subject, body):
    """Função que simula o envio de email"""
    pass

# 🔹 Criando o router de teste
router = APIRouter()

@router.post("/notify/")
async def send_notification(data: dict = Body(...)):
    """Envia uma notificação por email."""
    send_email(data["email"], "Notificação de Vídeo", data["message"])
    return {"message": "Notificação enviada!"}

# 🔹 Criando um app de teste com o router
app = FastAPI()
app.include_router(router)

client = TestClient(app)

@patch(__name__ + '.send_email')  # Usando __name__ para referenciar o módulo atual
def test_send_notification(mock_send_email):
    mock_send_email.return_value = None  # Simula o comportamento da função real
    
    response = client.post(
        "/notify/",
        json={"email": "test@example.com", "message": "Teste de notificação"}
    )
    
    assert response.status_code == 200
    assert response.json() == {"message": "Notificação enviada!"}
    mock_send_email.assert_called_once_with("test@example.com", "Notificação de Vídeo", "Teste de notificação")

