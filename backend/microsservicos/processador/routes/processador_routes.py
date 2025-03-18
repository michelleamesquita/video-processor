from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Header
from fastapi.responses import FileResponse
import os
import json
import jwt
import pika
from models.rabbitmq import RabbitMQ
from controllers.processador_controller import background_processing


router = APIRouter()

# 🔹 Variáveis de Configuração
TEST_MODE = os.getenv("TEST_MODE") == "True"
QUEUE_NAME = "video_processing"
STATUS_QUEUE = "video_status"
CANCELADOS = set()
SECRET_KEY = "secret123"

### 🔹 Função para validar o token JWT
async def verify_token(authorization: str = Header(None)):
    """Verifica o token JWT do usuário."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Token ausente")

    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Esquema de autenticação inválido")
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except ValueError:
        raise HTTPException(status_code=401, detail="Formato do token inválido")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


### 🔹 **Endpoint para iniciar o processamento do vídeo**
@router.post("/process-video/")

@router.post("/process-video/")
async def process_video_endpoint(video_id: str, video_path: str, background_tasks: BackgroundTasks, user=Depends(verify_token)):
    """ Inicia o processamento do vídeo apenas para usuários autenticados """
    print(f"🔹 Usuário autenticado: {user}")
    user_id = user.get("sub", None)
    user_email = user.get("email", None)

    if not user_id:
        raise HTTPException(status_code=400, detail="ID do usuário não encontrado no token")

    if not os.path.exists(video_path):
        raise HTTPException(status_code=400, detail="Arquivo de vídeo não encontrado")

    connection, channel = RabbitMQ.connect_rabbitmq()  # ✅ Agora pega `connection, channel` corretamente

    if channel:
        message = json.dumps({"video_id": video_id, "user_id": user_id, "user_email": user_email})
        channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=message, properties=pika.BasicProperties(delivery_mode=2))
        print(f"📩 Enviado vídeo {video_id} para processamento na fila `{QUEUE_NAME}`.")

    return {"message": "Processamento iniciado", "video_id": video_id, "user_id": user_id, "user_email": user_email}

### 🔹 **Endpoint para cancelar o processamento de um vídeo**
@router.post("/cancelar/{video_id}")
def cancelar_video(video_id: str, user=Depends(verify_token)):
    """Marca um vídeo como cancelado para interromper o processamento"""
    user_id = user["sub"]
    
    global CANCELADOS
    CANCELADOS.add(video_id)

    # Atualiza status no RabbitMQ para "canceled"
    RabbitMQ.publish_status(video_id, user_id, "canceled", user.get("email"))
    
    return {"message": f"O processamento do vídeo {video_id} foi cancelado."}


### 🔹 **Endpoint para verificar o status de um vídeo específico**
@router.get("/processar/status/{video_id}")
def get_video_status(video_id: str, user=Depends(verify_token)):
    """Verifica o status de um único vídeo"""
    connection,channel = RabbitMQ.connect_rabbitmq()
    if channel is None:
        return {"error": "Erro ao conectar ao RabbitMQ"}

    try:
        channel.queue_declare(queue=STATUS_QUEUE, durable=True)
        method_frame, header_frame, body = channel.basic_get(queue=STATUS_QUEUE, auto_ack=False)

        while body:
            message = json.loads(body)
            if message["video_id"] == video_id:
                channel.basic_nack(method_frame.delivery_tag, requeue=True)
                return {"video_id": video_id, "status": message["status"]}

            channel.basic_nack(method_frame.delivery_tag, requeue=True)
            method_frame, header_frame, body = channel.basic_get(queue=STATUS_QUEUE, auto_ack=False)

        return {"video_id": video_id, "status": "processing"}  # Se não encontrar, assume que ainda está em processamento

    except Exception as e:
        print(f"❌ Erro ao buscar status do vídeo {video_id}: {e}")
        return {"error": f"Erro ao buscar status do vídeo: {e}"}


### 🔹 **Endpoint para listar status de todos os vídeos do usuário**
@router.get("/videos/status/")
def list_videos_status(user=Depends(verify_token)):
    """Lista todos os status de vídeos de um usuário autenticado"""
    user_id = user["sub"]
    
    connection,channel = RabbitMQ.connect_rabbitmq() 
    if channel is None:
        print("❌ Erro ao conectar ao RabbitMQ")
        return {"error": "Erro ao conectar ao RabbitMQ"}

    videos = {}

    try:
        # ✅ Agora usa `channel` corretamente
        queue_state = channel.queue_declare(queue="video_status", passive=True)
        message_count = queue_state.method.message_count
        print(f"📩 Fila `video_status` contém {message_count} mensagens.")

        if message_count == 0:
            return {"user_id": user_id, "videos": []}

        for _ in range(message_count):
            method_frame, header_frame, body = channel.basic_get(queue="video_status", auto_ack=False)

            if body:
                message = json.loads(body.decode())  # ✅ Decodifica o JSON corretamente
                video_id = message["video_id"]

                if message.get("user_id") == user_id:
                    if video_id not in videos:
                        videos[video_id] = []
                    videos[video_id].append(message)

                channel.basic_nack(method_frame.delivery_tag)

    except Exception as e:
        print(f"❌ Erro ao buscar status dos vídeos: {e}")
        return {"error": f"Erro ao buscar status dos vídeos: {str(e)}"}

    finally:
        connection.close()  # ✅ Fecha a conexão após o uso

    return {"user_id": user_id, "videos": [{"video_id": v, "statuses": videos[v]} for v in videos]}



### 🔹 **Endpoint para baixar vídeos processados**
@router.get("/download/")
def download_video(video_id: str):
    """Faz o download do vídeo processado"""
    zip_path = f"/processed_videos/{video_id}.zip"
    if os.path.exists(zip_path):
        return FileResponse(zip_path, filename=f"{video_id}.zip", media_type="application/zip")
    raise HTTPException(status_code=404, detail="Arquivo não encontrado")


### 🔹 **Endpoint para verificar a saúde do sistema**
@router.get("/health")
def health_check():
    """Verifica se o sistema está rodando corretamente"""
    return {"status": "ok"}

