import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.consumer import SyncConsumer
import random
from .engine import GameEngine

class TictactoePlayerConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "tictactoe_game" #%s" % self.room_name
        self.game_engine_channel_name = "tictactoe_game_engine"
        self.username = f"user_{random.randint(0, 10000)}"
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.player_join()
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

        if msg_type == "player_join":
            self.player_join(content)
        elif msg_type == "update_color":
            self.update_color(content)
        else:
            raise ValueError(f"The type {msg_type} is not recognized")

    def update_color(self, content):
        new_color = content["value"]
        print(f"{self.username} update their color to {new_color}")
        async_to_sync(self.channel_layer.send)(
            self.game_engine_channel_name,
            {
                "type": "color.update",
                "new_color": new_color,
                "user_name": self.username,
            },
        )

    def player_join(self, content={}):
        async_to_sync(self.channel_layer.send)(
            self.game_engine_channel_name,
            {"type": "player.join", "user_name": self.username,},
        )

    def game_update(self, event):
        # Send message to WebSocket
        state = event["state"]
        async_to_sync(self.send(json.dumps(state)))

class TictactoeGameCustomer(SyncConsumer):
    def __init__(self, *args, **kwargs):
        """
        Created on demand when the first player joins.
        """
        print("Game Consumer: %s %s", args, kwargs)
        super().__init__(*args, **kwargs)
        self.group_name = "tictactoe_game"
        self.engine = GameEngine(self.group_name)
        self.engine.start()

    def color_update(self, message):
        # print(message)
        print("Test: " + message["new_color"])

    def player_join(self, message):
        user_name = message["user_name"]
        self.engine.player_join(user_name)
