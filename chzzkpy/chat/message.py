import datetime
from typing import Optional, Literal

from pydantic import AliasChoices, Field, Json

from .enums import ChatType
from .profile import Profile
from ..base_model import ChzzkModel


class Extra(ChzzkModel):
    chat_type: str
    emojis: str
    os_type: Literal['PC', 'AOS', 'IOS']
    streaming_channel_id: str


class Message(ChzzkModel):
    service_id: str = Field(validation_alias=AliasChoices('serviceId', 'svcid'))
    channel_id: str = Field(validation_alias=AliasChoices('channelId', 'cid'))
    user_id: str = Field(validation_alias=AliasChoices('uid', 'userId'))

    profile: Optional[Json[Profile]]
    content: str = Field(validation_alias=AliasChoices('msg', 'content'))
    type: ChatType = Field(validation_alias=AliasChoices('msgTypeCode', 'messageTypeCode'))
    extras: Optional[Json[Extra]]

    created_time: datetime.datetime = Field(validation_alias=AliasChoices('ctime', 'createTime'))
    updated_time: Optional[datetime.datetime] = Field(validation_alias=AliasChoices('utime', 'updateTime'))
    time: datetime.datetime = Field(validation_alias=AliasChoices('msgTime', 'messageTime'))


class NoticeMessage(Message):
    pass


class MessageExtendedMemberId(Message):
    member_id: int = Field(validation_alias=AliasChoices('mbrCnt', 'memberCount'))


class ChatMessage(MessageExtendedMemberId):
    message_status: Optional[str] = Field(validation_alias=AliasChoices('msgStatueType', 'messageStatusType'))

    # message_tid: ???
    # session: bool

    @property
    def is_blind(self) -> bool:
        return self.message_status == 'BLIND'
