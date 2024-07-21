from channels.routing import ProtocolTypeRouter, URLRouter
import os
import django
from django.urls import path
from django.core.asgi import get_asgi_application



application = get_asgi_application()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

# from chats.consumers import ChatConsumer







ws_urlpatterns = [
   
]
# application = ProtocolTypeRouter(
#     {
#         'http':asgi,
#         'websocket':URLRouter(ws_urlpatterns),
#     }
# )