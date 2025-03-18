from models.notificacao import NotificationRequest
from models.email_service import send_email

def process_notification(notification: NotificationRequest):
    """Processa o envio de uma notificação."""
    send_email(notification.email, "Notificação de Vídeo", notification.message)
    return {"message": "Notificação enviada com sucesso!"}
