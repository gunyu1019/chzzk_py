import asyncio
import logging
from typing import Optional, Callable

import aiohttp

from .access_token import AccessToken
from .gateway import ChzzkWebSocket
from ..client import Client

_log = logging.getLogger(__name__)


class ChatClient(Client):
    def __init__(
            self,
            channel_id: str,
            authorization_key: Optional[str] = None,
            session_key: Optional[str] = None,
            chat_channel_id: Optional[str] = None,
            loop: Optional[asyncio.AbstractEventLoop] = None
    ):
        super().__init__(loop=loop, authorization_key=authorization_key, session_key=session_key)

        self.chat_channel_id: str = chat_channel_id
        self.channel_id: str = channel_id
        self.access_token: Optional[AccessToken] = None
        self.user_id: Optional[str] = None

        self.ws_session = aiohttp.ClientSession()
        self._closed = False

        self._listeners: dict[str, list[asyncio.Future, Callable[..., bool]]] = dict()

        self._gateway: Optional[ChzzkWebSocket] = None

    async def _generate_access_token(self) -> AccessToken:
        res = await self._game_session.chat_access_token(channel_id=self.chat_channel_id)
        self.access_token = res.content
        return self.access_token

    @property
    def is_connected(self) -> bool:
        return self._gateway.connected

    @property
    def is_closed(self) -> bool:
        return self._closed

    async def connect(self, reconnect: bool = True) -> None:
        if self.chat_channel_id is None:
            status = await self.live_status(channel_id=self.channel_id)
            self.chat_channel_id = status.chat_channel_id

        if self._game_session.has_login:
            user = await self.user()
            self.user_id = user.user_id_hash

        if self.access_token is None:
            await self._generate_access_token()

        await self.polling()

    async def close(self):
        await self._gateway.socket.close()
        await self.ws_session.close()
        await super().close()

    async def polling(self):
        initial_connect = True
        session_id: Optional[str] = None
        while not self.is_closed:
            self._gateway = await ChzzkWebSocket.from_client(
                self,
                initial=initial_connect,
                session_id=session_id
            )

            if initial_connect or session_id is None:
                await self._gateway.send_open(
                    access_token=self.access_token.access_token,
                    chat_channel_id=self.chat_channel_id,
                    mode="READ" if self.user_id is None else "SEND",
                    user_id=self.user_id
                )
                session_id = self._gateway.session_id
            initial_connect = False

            while True:
                await self._gateway.poll_event()
