import pika
import json
import os
from services.notification_service import NotificationService

RABBITMQ_HOST = "rabbitmq"
QUEUE_NAME = "video_processing"
STATUS_QUEUE = "video_status"
TEST_MODE = os.getenv("TEST_MODE") == "True"

class RabbitMQ:
    """Classe para gerenciar conexões e publicação de mensagens no RabbitMQ"""

    @staticmethod
    def connect_rabbitmq():
        """Conecta ao RabbitMQ e retorna um **canal**"""

        if TEST_MODE:
            return None,None  # Retorna tupla vazia para evitar erros no modo de teste

        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
            channel = connection.channel()
            channel.queue_declare(queue=QUEUE_NAME, durable=True)
            channel.queue_declare(queue=STATUS_QUEUE, durable=True)
            return connection,channel  # ✅ Retorna os dois objetos corretamente
        except Exception as e:
            print(f"❌ Erro ao conectar ao RabbitMQ: {e}")
            return None

    @staticmethod
    def publish_status(video_id, user_id, status, user_email):
        """Publica o status do vídeo no RabbitMQ"""
        if TEST_MODE:
            print(f"[TESTE] Mock: Status publicado para {video_id}: {status}")
            return

        connection,channel = RabbitMQ.connect_rabbitmq()
        if channel is None:
            print("❌ Erro ao conectar ao RabbitMQ para publicar status!")
            return

        channel.queue_declare(queue=STATUS_QUEUE, durable=True)

        message = json.dumps({
            "video_id": video_id,
            "user_id": user_id,
            "status": status
        })

        channel.basic_publish(
            exchange='',
            routing_key=STATUS_QUEUE,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)  # 🔹 Persistência de mensagens
        )

        print(f"📩 Status atualizado para {video_id}: {status}")


        # 🔹 Enviar notificação para o usuário, se necessário
        if user_email and status in ["processed", "error", "canceled"]:
            msg = {
                "processed": f"✅ Seu vídeo {video_id} foi processado com sucesso!",
                "error": f"❌ Houve um erro no processamento do seu vídeo {video_id}.",
                "canceled": f"⏹️ O processamento do seu vídeo {video_id} foi cancelado."
            }.get(status, "")

            NotificationService.send_notification(user_email, msg)

    @staticmethod
    def get_status_messages():
        """Obtém mensagens da fila de status"""
        connection, channel = RabbitMQ.connect_rabbitmq()
        if channel is None:
            return []

        messages = []
        try:
            channel.queue_declare(queue=STATUS_QUEUE, durable=True)

            while True:
                method_frame, header_frame, body = channel.basic_get(queue=STATUS_QUEUE, auto_ack=True)
                if not body:
                    break  # Sai do loop quando não houver mais mensagens
                message = json.loads(body)
                messages.append(message)

                channel.basic_ack(method_frame.delivery_tag)

        except Exception as e:
            print(f"❌ Erro ao buscar status do vídeo: {e}")

        finally:
            connection.close()  # ✅ Fecha conexão ao finalizar

        return messages
