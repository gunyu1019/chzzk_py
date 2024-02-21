import aiohttp

from .access_token import AccessToken
from ..client import Client


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

        self._default = {
            "cid": self.chat_channel_id,
            "svcid": "game",
            "ver": "2"
        }

    async def _generate_access_token(self) -> AccessToken:
        self.access_token = await self._game_session.chat_access_token(channel_id=self.chat_channel_id)
        return self.access_token

    @property
    def is_connected(self) -> bool:
        return self._connected

    async def connect(self):
        if self.chat_channel_id is None:
            status = await self.live_status(self.channel_id)
            self._default['cid'] = self.chat_channel_id = status.chat_channel_id

        if self.access_token is None:
            await self._generate_access_token()

        if self._game_session.has_login:
            user = await self.user()
            self._uid = user.user_id_hash

        server_id = abs(sum([ord(x) for x in self.chat_channel_id])) % 9 + 1
        url = f"wss://kr-ss{server_id}.chat.naver.com/chat"
        return
