# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.consumer import SyncConsumer
import random


class TictactoePlayerConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "tictactoe_%s" % self.room_name
        self.game_engine_channel_name = "tictactoe_game_engine"
        self.username = f"user_{random.randint(0, 10000)}"
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        content = json.loads(text_data)
        msg_type = content["type"]

        if msg_type == "update_color":
            new_color = content["value"]
            print(f"{self.username} update their color to {new_color}")
            async_to_sync(self.channel_layer.send)(
            self.game_engine_channel_name, {"type": "color.update", "new_color": new_color}
        )
        else:
            raise ValueError(f"The type {msg_type} is not recognized")
        # async_to_sync(self.channel_layer.group_send)(
        #     self.room_group_name, {"type": "chat_message", "message": message}
        # )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(message)


class TictactoeGameCustomer(SyncConsumer):
    def __init__(self, *args, **kwargs):
        """
        Created on demand when the first player joins.
        """
        print("Game Consumer: %s %s", args, kwargs)
        super().__init__(*args, **kwargs)
        self.channel_name = "tictactoe_game_engine"
        # self.engine = GameEngine(self.group_name)
        # self.engine.start()

    def color_update(self, message):
        # print(message)
        print("Test: " + message['new_color'])