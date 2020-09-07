from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter

from kcsec.chat import routing as chat_routing

application = ProtocolTypeRouter({"websocket": AuthMiddlewareStack(URLRouter(chat_routing.websocket_urlpatterns))})
