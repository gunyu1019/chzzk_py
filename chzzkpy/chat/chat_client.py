from typing import Any

import aiohttp
import asyncio
import logging

from .access_token import AccessToken
from .enums import ChatCmd, get_enum
from ..client import Client

_log = logging.getLogger(__name__)


class ChatClient(Client):
    def __init__(
            self,
            channel_id: str,
            authorization_key: str = None,
            session_key: str = None,
            chat_channel_id: str = None
    ):
        super().__init__(authorization_key, session_key)

        self.chat_channel_id: str = chat_channel_id
        self.channel_id: str = channel_id
        self.access_token: AccessToken | None = None

        self._uid: str | None = None
        self._sid: str | None = None

        self._ws_session = aiohttp.ClientSession()
        self._connected = False
        self._closed = False

        self._default = {
            "cid": self.chat_channel_id,
            "svcid": "game",
            "ver": "2"
        }
        self.__ws: aiohttp.ClientWebSocketResponse | None = None

    async def _generate_access_token(self) -> AccessToken:
        res = await self._game_session.chat_access_token(channel_id=self.chat_channel_id)
        self.access_token = res.content
        return self.access_token

    @property
    def is_connected(self) -> bool:
        return self._connected

    @property
    def is_closed(self) -> bool:
        return self._closed

    async def connect(self, reconnect: bool = True) -> None:
        if self.chat_channel_id is None:
            status = await self.live_status(self.channel_id)
            self._default['cid'] = self.chat_channel_id = status.chat_channel_id

        if self._game_session.has_login:
            user = await self.user()
            self._uid = user.user_id_hash

        await self.polling(reconnect)

    async def close(self):
        self._closed = True
        await self.__ws.close()
        await super().close()

    async def polling(self, reconnect: bool = True):
        server_id = abs(sum([ord(x) for x in self.chat_channel_id])) % 9 + 1
        url = f"wss://kr-ss{server_id}.chat.naver.com/chat"

        while not self.is_closed:
            try:
                await self._generate_access_token()

                self.__ws = await self._ws_session.ws_connect(url)

                while True:
                    await self.poll_event()
            except asyncio.TimeoutError:
                # disconnect
                if not reconnect:
                    await self.close()
                    return

                if self.is_closed:
                    return

    async def poll_event(self):
        try:
            msg = await asyncio.wait_for(self.__ws.receive(), timeout=30.0)
            if msg.type is aiohttp.WSMsgType.TEXT:
                data = await msg.json()
                await self.receive_message(data)
        except asyncio.TimeoutError:
            pass

    async def receive_message(self, data: dict[str, Any]) -> None:
        cmd: int = data['cmd']
        body = data.get('bdy')

        cmd_type = get_enum(ChatCmd, cmd)

        if cmd_type == ChatCmd.CONNECTED:
            self._connected = True
            self._sid = body['sid']
        elif cmd_type == ChatCmd.PING:
            await self._ws_pong()
        elif cmd_type == ChatCmd.CHAT:
            pass
        elif cmd_type == ChatCmd.RECENT_CHAT:
            pass
        elif cmd_type == ChatCmd.DONATION:
            pass
        elif cmd_type == ChatCmd.NOTICE:
            pass
        elif cmd_type == ChatCmd.BLIND:
            pass

    async def _ws_pong(self):
        await self.__ws.send_json({
            'cmd': ChatCmd.PONG,
            'ver': 2
        })
