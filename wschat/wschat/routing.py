from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path, path
from chat import consumers

# URLs that handle the WebSocket connection are placed here.
websocket_urlpatterns=[
                    path("chat/<str:chat_box_name>/", consumers.ChatRoomConsumer.as_asgi()),
                    #re_path(r"ws/chat/(?P<chat_box_name>\w+)/$", consumers.ChatRoomConsumer.as_asgi()),
                ]

application = ProtocolTypeRouter( 
    {
        "websocket": AuthMiddlewareStack(
            URLRouter(
               websocket_urlpatterns
            )
        ),
    }
)
