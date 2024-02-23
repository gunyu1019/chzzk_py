import datetime
from typing import Literal, Optional, Any
from pydantic import Field, Json

from .enums import ChatCmd, ChatType, UserRole
from .ws_message import WSMessageBase
from ..base_model import ChzzkModel


class Extra(ChzzkModel):
    chat_type: str
    emoji: str
    os_type: Literal['PC', 'AOS', 'IOS']
    streaming_channel_id: str


class StreamingProperty(ChzzkModel):
    pass


class Profile(ChzzkModel):
    activity_badges: list[Any]
    user_id_hash: str
    user_role: UserRole = Field(alias='user_role_code')
    nickname: str
    profile_image_url: Optional[str]
    badge: ...
    title: ...
    streaming_property: StreamingProperty
    verified_mark: bool


class Message(WSMessageBase):
    member_count: int = Field(alias="mbrCnt")
    user_id: str = Field(alias="uid")
    profile: Json[...]
    message: str = Field(alias='msg')
    message_type: ChatType
    extras: Json[Extra]
    created_time: datetime.datetime
    updated_time: datetime.datetime
    # message_tid: ???
    session: bool
    time: datetime.datetime = Field(alias='msgTime')


class WSMessageChat(WSMessageBase):
    body: list[Message] = Field(alias='bdy')
