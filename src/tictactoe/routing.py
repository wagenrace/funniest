# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/tictactoe/(?P<room_name>\w+)/$', consumers.TictactoePlayerConsumer),
]