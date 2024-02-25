from async_client_decorator import get, Query
from typing import Annotated

from .access_token import AccessToken
from ..base_model import Content
from ..http import (
    ChzzkSession,
    NaverGameAPISession,
    _response_pydantic_model_validation_able,
    _custom_query_name,
    _response_pydantic_model_validation
)


class ChzzkChatSession(NaverGameAPISession):
    @_response_pydantic_model_validation_able
    @ChzzkSession.logging
    @_custom_query_name("channel_id", "channelId")  # Will moved. (Temporary Decorator)
    @ChzzkSession.login_able
    @get("/nng_main/v1/chats/access-token")
    @Query.default_query("chatType", "STREAMING")
    @_response_pydantic_model_validation
    async def chat_access_token(
        self, channel_id: Annotated[str, Query]
    ) -> Content[AccessToken]:
        pass
