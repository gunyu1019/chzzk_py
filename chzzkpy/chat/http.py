from ahttp_client import get, Query
from ahttp_client.extension import get_pydantic_response_model
from typing import Annotated

from .access_token import AccessToken
from ..base_model import Content
from ..http import (
    ChzzkSession,
    NaverGameAPISession
)


class ChzzkChatSession(NaverGameAPISession):
    @get_pydantic_response_model()
    @get("/nng_main/v1/chats/access-token", directly_response=True)
    @ChzzkSession.configuration(login_able=True)
    @Query.default_query("chatType", "STREAMING")
    async def chat_access_token(
        self, channel_id: Annotated[str, Query.to_camel()]
    ) -> Content[AccessToken]:
        pass
