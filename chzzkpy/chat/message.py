"""MIT License

Copyright (c) 2024 gunyu1019

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import datetime
from typing import Optional, Literal, TypeVar, Generic, Any
from pydantic import AliasChoices, Field, Json

from .enums import ChatType
from .profile import Profile
from ..base_model import ChzzkModel

E = TypeVar("E", bound="ExtraBase")


class ExtraBase(ChzzkModel):
    pass


class Extra(ExtraBase):
    chat_type: str
    emojis: Any
    os_type: Literal["PC", "AOS", "IOS"]
    streaming_channel_id: str


class Message(ChzzkModel, Generic[E]):
    service_id: str = Field(validation_alias=AliasChoices("serviceId", "svcid"))
    channel_id: str = Field(validation_alias=AliasChoices("channelId", "cid"))
    user_id: str = Field(validation_alias=AliasChoices("uid", "userId"))

    profile: Optional[Json[Profile]]
    content: str = Field(validation_alias=AliasChoices("msg", "content"))
    type: ChatType = Field(
        validation_alias=AliasChoices("msgTypeCode", "messageTypeCode")
    )
    extras: Optional[Json[E]]

    created_time: datetime.datetime = Field(
        validation_alias=AliasChoices("ctime", "createTime")
    )
    updated_time: Optional[datetime.datetime] = Field(
        default=None, validation_alias=AliasChoices("utime", "updateTime")
    )
    time: datetime.datetime = Field(
        validation_alias=AliasChoices("msgTime", "messageTime")
    )


class MessageDetail(Message[E], Generic[E]):
    member_count: int = Field(validation_alias=AliasChoices("mbrCnt", "memberCount"))
    message_status: Optional[str] = Field(
        validation_alias=AliasChoices("msgStatusType", "messageStatusType")
    )

    # message_tid: ???
    # session: bool

    @property
    def is_blind(self) -> bool:
        return self.message_status == "BLIND"


class ChatMessage(MessageDetail[Extra]):
    pass


class NoticeExtra(Extra):
    register_profile: Profile


class NoticeMessage(Message[NoticeExtra]):
    pass


class DonationRank(ChzzkModel):
    user_id_hash: str
    nickname: str = Field(validation_alias=AliasChoices("nickname", "nickName"))
    verified_mark: bool
    donation_amount: int
    ranking: int


class DonationExtra(ExtraBase):
    is_anonymous: bool = True
    pay_type: str
    pay_amount: int = 0
    donation_type: str
    weekly_rank_list: Optional[list[DonationRank]] = Field(default_factory=list)
    donation_user_weekly_rank: Optional[DonationRank] = None


class DonationMessage(MessageDetail[DonationExtra]):
    pass


class SystemExtraParameter(ChzzkModel):
    register_nickname: str
    target_nickname: str
    register_chat_profile: Json[Profile] = Field(alias="registerChatProfileJson")
    target_profile: Json[Profile] = Field(alias="targetChatProfileJson")


class SystemExtra(ExtraBase):
    description: str
    style_type: int
    visible_roles: list[str]
    params: Optional[SystemExtraParameter] = None


class SystemMessage(MessageDetail[SystemExtra]):
    pass
