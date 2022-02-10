from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path,include
from chat.consumers import EchoConsumer, ChatConsumer
from channels.auth import AuthMiddlewareStack
from chat.views import template_view
application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/chat/<str:username>/', ChatConsumer),
            path('ws/chat/', EchoConsumer),
            # path('',template_view , name="ho"),
            # path()
        ])
    )
})