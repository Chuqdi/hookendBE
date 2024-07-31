import os
from django.core.asgi import get_asgi_application

from likes.consumers import LikeLiveUpdateConsumer




asgi_application = get_asgi_application()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from django.urls import path

from chats.consumers import ChatConsumer, OnlineStatus

websocket_url_patterns =[
    path("ws/chat/onlineStatus/", OnlineStatus.as_asgi()),
    path("ws/likeUpdate/", LikeLiveUpdateConsumer.as_asgi()),
    path("ws/chat/<str:sender_id>/<str:reciever_id>/", ChatConsumer.as_asgi()),
]
application = ProtocolTypeRouter(
    {
        "http": asgi_application,
        "websocket": AuthMiddlewareStack(URLRouter(
           websocket_url_patterns,
        )),
    }
)


