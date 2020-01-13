# chat/routing.py
from django.urls import re_path

#from .consumers import ChatConsumer
from . import consumers

websocket_urlpatterns = [
    re_path(r'chat/(?P<room_name>\w+)/$', consumers.ChatConsumer),
]
# websocket_urlpatterns = [
#       url(r'^ws/chat/$', consumers.ChatConsumer')
# ]
