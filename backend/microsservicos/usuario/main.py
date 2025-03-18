from fastapi import FastAPI
from routes.usuario_routes import router as usuario_router
from models.database import Base, engine

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Incluir rotas de usuário
app.include_router(usuario_router)

@app.get("/health")
def health_check():
    """Verifica se o servidor está rodando corretamente."""
    return {"status": "ok"}
