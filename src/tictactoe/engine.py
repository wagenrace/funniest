import logging
import random
import threading
import time
import uuid
from collections import OrderedDict, deque
from typing import Mapping, Optional, Set, Tuple

import attr
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

log = logging.getLogger(__name__)


class GameEngine(threading.Thread):
    def __init__(self, group_name, **kwargs):
        log.info("Init GameEngine...")
        super(GameEngine, self).__init__(daemon=True, name="GameEngine", **kwargs)
        self.name = uuid.uuid4()
        self.group_name = group_name
        self.channel_layer = get_channel_layer()
        self.direction_lock = threading.Lock()
        self.player_queue = OrderedDict()
        self.player_lock = threading.Lock()
        self.users = []

    def run(self) -> None:
        log.info("Starting engine loop")

    def player_join(self, user_name: str) -> None:
        self.users.append(user_name)
        self.send_state()

    def send_state(self):
        state_json = {"users": self.users}
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {"type": "game_update", "state": state_json}
        )
