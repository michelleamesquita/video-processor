from fastapi import FastAPI
from routes.notificacao_routes import router

app = FastAPI()

app.include_router(router)

@app.get("/health")
def health_check():
    """Verifica se o serviço está rodando."""
    return {"status": "ok"}
