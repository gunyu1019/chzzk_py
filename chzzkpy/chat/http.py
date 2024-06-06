import asyncio

from ahttp_client import Session, get, post, delete, Query
from ahttp_client.request import RequestCore
from ahttp_client.extension import get_pydantic_response_model
from typing import Annotated, Optional

from .access_token import AccessToken
from ..base_model import Content
from ..http import ChzzkSession, NaverGameAPISession


class ChzzkChatSession(NaverGameAPISession):
    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None):
        super().__init__(loop=loop)

        self.delete_notice_message.before_hook(ChzzkChatSession.query_to_json)
        self.set_notice_message.before_hook(ChzzkChatSession.query_to_json)
        self.blind_message.before_hook(ChzzkChatSession.query_to_json)

    @get_pydantic_response_model()
    @get("/nng_main/v1/chats/access-token", directly_response=True)
    @ChzzkSession.configuration(login_able=True)
    @Query.default_query("chatType", "STREAMING")
    async def chat_access_token(
        self, channel_id: Annotated[str, Query.to_camel()]
    ) -> Content[AccessToken]:
        pass

    async def query_to_json(session: Session, request: RequestCore, path: str):
        copied_request_obj = request.copy()
        body = dict()
        for key, value in request.params.copy().items():
            body[key] = value
        copied_request_obj.params = dict()
        copied_request_obj.body = body
        return copied_request_obj, path

    @get_pydantic_response_model()
    @delete("/nng_main/v1/chats/notices", directly_response=True)
    @ChzzkSession.configuration(login_able=True, login_required=True)
    @Query.default_query("chatType", "STREAMING")
    async def delete_notice_message(
        self, channel_id: Annotated[str, Query.to_camel()]
    ) -> Content[None]:
        pass

    @get_pydantic_response_model()
    @post("/nng_main/v1/chats/notices", directly_response=True)
    @ChzzkSession.configuration(login_able=True, login_required=True)
    @Query.default_query("chatType", "STREAMING")
    async def set_notice_message(
        self,
        channel_id: Annotated[str, Query.to_camel()],
        extras: Annotated[str, Query],
        message: Annotated[str, Query],
        message_time: Annotated[int, Query.to_camel()],
        message_user_id_hash: Annotated[int, Query.to_camel()],
        streaming_channel_id: Annotated[int, Query.to_camel()],
    ) -> Content[None]:
        return

    @get_pydantic_response_model()
    @post("/nng_main/v1/chats/blind-message", directly_response=True)
    @ChzzkSession.configuration(login_able=True, login_required=True)
    @Query.default_query("chatType", "STREAMING")
    async def blind_message(
        self,
        channel_id: Annotated[str, Query.to_camel()],
        message: Annotated[str, Query],
        message_time: Annotated[int, Query.to_camel()],
        message_user_id_hash: Annotated[int, Query.to_camel()],
        streaming_channel_id: Annotated[int, Query.to_camel()],
    ) -> Content[None]:
        pass
