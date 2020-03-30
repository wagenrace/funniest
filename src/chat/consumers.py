# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message
import random


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        if not "seed" in self.scope["session"].keys():
            self.scope["session"]["seed"] = random.randint(1, 1000)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.secret_words = {
            "apple": False,
            "pear": False,
            "cat": False,
        }
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        if message in self.secret_words.keys():
            self.secret_words[message] = True
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(message)

    def send(self, message):
        """
        Sends a reply back down the WebSocket
        """

        # message = "List of guessed words\n"
        # for i in self.secret_words:
        #     if self.secret_words[i]:
        #         message += f"The word {i} is found\n"
        username = self.scope['session']['seed']
        message = f"{username}: {message}"
        text_data = json.dumps({"message": message})
        print(text_data)
        super().send( text_data = text_data)
