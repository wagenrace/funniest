from channels.routing import ChannelNameRouter, ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack
import chat.routing
import tictactoe.routing
from tictactoe.consumers import TictactoeGameCustomer

application = ProtocolTypeRouter(
    {
        # (http->django views is added by default)
        "websocket": SessionMiddlewareStack(
            URLRouter(tictactoe.routing.websocket_urlpatterns,)
        ),
        "channel": ChannelNameRouter({"tictactoe_game_engine": TictactoeGameCustomer}),
    }
)
