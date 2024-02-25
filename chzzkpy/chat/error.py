import aiohttp
from typing import Optional


class ConnectionClosed(Exception):
    def __init__(
        self, socket: aiohttp.ClientWebSocketResponse, code: Optional[int] = None
    ):
        self.code: int = code or socket.close_code or -1
        self.reason: str = ""
        super().__init__(f"WebSocket closed with {self.code}")


class WebSocketClosure(Exception):
    pass


class ReconnectWebsocket(Exception):
    pass
