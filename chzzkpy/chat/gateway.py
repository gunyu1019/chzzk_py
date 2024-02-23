import asyncio
import datetime
import json
import logging
import time
from typing import Any, Callable, Coroutine, Optional, Literal, Self, TYPE_CHECKING

import aiohttp

from .enums import ChatCmd, get_enum, ChatType
from .error import ConnectionClosed, WebSocketClosure, ReconnectWebsocket

if TYPE_CHECKING:
    from .chat_client import ChatClient

_log = logging.getLogger(__name__)


class ChzzkWebSocket:
    def __init__(
            self,
            socket: aiohttp.ClientWebSocketResponse,
            loop: asyncio.AbstractEventLoop,
            hook: Callable[..., Coroutine[Any, Any, Any]] = None,
    ):
        self.socket: aiohttp.ClientWebSocketResponse = socket
        self.loop: asyncio.AbstractEventLoop = loop

        self._connected: bool = False
        self.session_id: Optional[str] = None

        self._max_timeout: float = 60.0

        if hook is not None:
            self._hook = hook

    @classmethod
    async def from_client(
            cls,
            client: "ChatClient",
            session_id: Optional[str] = None
    ) -> Self:
        server_id = abs(sum([ord(x) for x in client.chat_channel_id])) % 9 + 1
        url = f"wss://kr-ss{server_id}.chat.naver.com/chat"
        socket: aiohttp.ClientWebSocketResponse = await client.ws_session.ws_connect(url)

        websocket = cls(socket, client.loop)
        websocket.session_id = session_id
        return websocket

    @property
    def default_body(self) -> dict[str, str]:
        return {
            "svcid": "game",
            "ver": "2"
        }

    @property
    def connected(self) -> bool:
        return self._connected

    async def _hook(self, evnet: ChatCmd, data: dict[str, Any]) -> None:
        pass

    def _can_handle_close(self, code: Optional[int] = None) -> bool:
        if code is None:
            code = self.socket.close_code
        return code != 1000

    async def poll_event(self):
        try:
            msg = await self.socket.receive(timeout=59.0)
            if msg.type is aiohttp.WSMsgType.TEXT:
                data = msg.json()
                await self.received_message(data)
            elif msg.type is aiohttp.WSMsgType.ERROR:
                _log.debug('Received error %s', msg)
                raise WebSocketClosure
            elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.CLOSING, aiohttp.WSMsgType.CLOSE):
                _log.debug('Received %s', msg)
                raise WebSocketClosure
        except asyncio.TimeoutError:
            await self.send_ping()
            _log.debug('Timeout receiving packet. Send to ping for keep-alive')
        except WebSocketClosure:
            code = self.socket.close_code
            if self._can_handle_close(code):
                raise ReconnectWebsocket()
            else:
                raise ConnectionClosed(self.socket, code)

    async def received_message(self, data: dict[str, Any]) -> None:
        cmd: int = data['cmd']
        body = data.get('bdy')

        cmd_type = get_enum(ChatCmd, cmd)
        _log.debug("Received Message: %s", data)

        if cmd_type == ChatCmd.CONNECTED:
            self._connected = True
            self.session_id = body['sid']
        elif cmd_type == ChatCmd.PING:
            await self.send_pong()
        else:
            await self._hook(cmd_type, data)

    async def send(self, data: str) -> None:
        _log.debug("Sending data: %s", data)
        await self.socket.send_str(data)

    async def send_json(self, data: dict[str, Any]) -> None:
        _log.debug("Sending JSON: %s", json.dumps(data))
        await self.socket.send_json(data)

    async def send_pong(self):
        await self.send_json({
            'cmd': ChatCmd.PONG,
            'ver': 2
        })

    async def send_ping(self):
        await self.send_json({
            'cmd': ChatCmd.PING,
            'ver': 2
        })

    async def send_open(
            self,
            access_token: str,
            chat_channel_id: str,
            mode: Literal['SEND', 'READ'],
            user_id: Optional[str] = None
    ):
        data: dict[str, Any] = {
            "bdy": {
                "accTkn": access_token,
                "auth": mode,
                "devType": 2001,
                "uid": user_id
            },
            "cid": chat_channel_id,
            "cmd": ChatCmd.CONNECT,
            "tid": 1
        }
        data.update(self.default_body)
        await self.send_json(data)

    async def send_chat(
            self,
            message: str,
            chat_channel_id: str
    ):
        extra: dict[str, Any] = {
            "chatType": "STREAMING",
            "emojis": "",
            "osType": "PC",
            "streamingChannelId": chat_channel_id
        }

        data: dict[str, Any] = {
            "bdy": {
                "extras": json.dumps(extra),
                "msg": message,
                "msgTime": int(time.time() * 1000),
                "msgTypeCode": ChatType.TEXT
            },
            "retry": False,
            "cmd": ChatCmd.SEND_CHAT,
            "sid": self.session_id,
            "cid": chat_channel_id,
            "tid": 3,
        }
        data.update(self.default_body)
        await self.send_json(data)
