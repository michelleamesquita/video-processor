from fastapi import APIRouter
from models.notificacao import NotificationRequest
from controllers.notificacao_controller import process_notification

router = APIRouter()

@router.post("/notify/")
def notify_user(notification: NotificationRequest):
    """Rota para enviar notificações por e-mail."""
    return process_notification(notification)
