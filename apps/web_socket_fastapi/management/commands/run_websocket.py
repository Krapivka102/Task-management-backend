from django.core.management.base import BaseCommand
import uvicorn
from apps.web_socket_fastapi.main import app

class Command(BaseCommand):
    help = "Запуск WebSocket-сервера (FastAPI)"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("🚀 Запускаем FastAPI WebSocket..."))
        uvicorn.run("apps.web_socket_fastapi.main:app", host="0.0.0.0", port=8001, reload=True)