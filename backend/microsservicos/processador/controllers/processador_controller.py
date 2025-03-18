import os
import threading
import json
import asyncio
import pika
from models.video import Video
from models.rabbitmq import RabbitMQ
from fastapi import HTTPException

CANCELADOS = set()

# Configuração do RabbitMQ
RABBITMQ_HOST = "rabbitmq"
QUEUE_NAME = "video_processing"

async def background_processing(video_id, video_path, user_id, user_email):
    """Executa o processamento do vídeo dentro do loop assíncrono corretamente."""
    try:
        output_folder = f"/processed_videos/{video_id}"
        zip_path = await Video.process_video(video_path, output_folder)
        
        # 🔹 Agora publica corretamente "processed"
        RabbitMQ.publish_status(video_id, user_id, "processed", user_email)
        print(f"✅ Vídeo {video_id} processado e status atualizado para 'processed'.")

    except Exception as e:
        print(f"❌ Erro no processamento do vídeo {video_id}: {e}")
        RabbitMQ.publish_status(video_id, user_id, "error", user_email)

def consume_video_queue():
    """Consumidor para processar vídeos em segundo plano."""
    connection, channel = RabbitMQ.connect_rabbitmq()  # ✅ Correção: Agora desembrulha a tupla corretamente
    
    if connection is None or channel is None:
        print("❌ Erro ao conectar ao RabbitMQ. O consumidor não será iniciado.")
        return

    channel.queue_declare(queue="video_processing", durable=True)

    def callback(ch, method, properties, body):
        """Função que processa cada mensagem da fila de processamento."""
        message = json.loads(body)
        video_id = message["video_id"]
        user_id = message["user_id"]
        user_email = message["user_email"]
        video_path = f"/app/{video_id}.mp4"

        print(f"📌 Processando vídeo: {video_id}")

        if video_id in CANCELADOS:
            print(f"⏹️ Processamento cancelado: {video_id}")
            RabbitMQ.publish_status(video_id, user_id, "canceled", user_email)
            CANCELADOS.remove(video_id)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        RabbitMQ.publish_status(video_id, user_id, "processing", user_email)

        try:
            asyncio.run(background_processing(video_id, video_path, user_id, user_email))
            RabbitMQ.publish_status(video_id, user_id, "processed", user_email)  # 🔹 Garante que o status final seja salvo
            ch.basic_ack(delivery_tag=method.delivery_tag)  # 🔹 Confirma o processamento
        except Exception as e:
            print(f"❌ Erro no processamento: {e}")
            RabbitMQ.publish_status(video_id, user_id, "error", user_email)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    channel.basic_consume(queue="video_processing", on_message_callback=callback)
    print("🎬 Aguardando mensagens na fila...")
    channel.start_consuming()
