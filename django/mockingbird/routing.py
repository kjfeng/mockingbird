# from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
import chat.routing
#  websocket urls in chat
#from chat import routing

# application = ProtocolTypeRouter({
#     # (http->django views is added by default)
#     'websocket': AllowedHostsOriginValidator(
#             AuthMiddlewareStack(
#                 URLRouter(
#                     routing.websocket_urlpatterns
#                 )
#             ),
#     )
# })

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': URLRouter(
                    chat.routing.websocket_urlpatterns
                    ),
})
