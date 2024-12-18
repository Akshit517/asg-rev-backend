from channels.routing import ProtocolTypeRouter, URLRouter
from chats.routing import websocket_urlpatterns
from django.core.asgi import get_asgi_application
from chats.middleware.channel_jwt_auth_middleware import JWTAuthMiddlewareStack

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': JWTAuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )
})