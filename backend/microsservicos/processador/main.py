from fastapi import FastAPI
from routes.processador_routes import router
import threading
from controllers.processador_controller import consume_video_queue

app = FastAPI()

# Adiciona as rotas ao app
app.include_router(router)

@app.get("/health")
def health_check():
    """Verifica se o serviço está ativo"""
    return {"status": "ok"}

# 🔹 Inicia a thread para consumir mensagens do RabbitMQ
worker_thread = threading.Thread(target=consume_video_queue, daemon=True)
worker_thread.start()
