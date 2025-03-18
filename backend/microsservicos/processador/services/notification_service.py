import requests
import os

NOTIFICATIONS_SERVICE_URL = "http://notificacoes:8004/notify/"

class NotificationService:
    """Classe para gerenciar notificações"""

    @staticmethod
    def send_notification(email, message):
        """Envia uma notificação para o usuário"""
        if os.getenv("TEST_MODE"):
            print(f"🔹 [TESTE] Mock: Envio de notificação para {email} - {message}")
            return

        print(f"📨 Enviando notificação para {email}: {message}")
        payload = {"email": email, "message": message}
        
        try:
            response = requests.post(NOTIFICATIONS_SERVICE_URL, json=payload)
            if response.status_code == 200:
                print(f"✅ Notificação enviada com sucesso para {email}!")
            else:
                print(f"❌ Erro ao enviar notificação: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Erro ao conectar ao serviço de notificações: {e}")
