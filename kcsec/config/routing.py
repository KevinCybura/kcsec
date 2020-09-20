from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter

from kcsec.chat import routing as chat_routing
from kcsec.crypto import routing as crypto_routing

application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(URLRouter(crypto_routing.websocket_urlpatterns)),
    },
)
