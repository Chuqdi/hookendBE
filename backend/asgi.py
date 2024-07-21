import os
from django.core.asgi import get_asgi_application




os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
asgi_application = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from django.urls import path

from chats.consumers import ChatConsumer, OnlineStatus

websocket_url_patterns =[
    path("ws/chat/<str:sender_id>/<str:reciever_id>/", ChatConsumer.as_asgi()),
    path("ws/chat/onlineStatus/", OnlineStatus.as_asgi())
]
application = ProtocolTypeRouter(
    {
        "http": asgi_application,
        "websocket": AuthMiddlewareStack(URLRouter(
           websocket_url_patterns,
        )),
    }
)


