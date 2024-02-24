from typing import Literal, Optional
from pydantic import Field

from .enums import ChatCmd
from .message import ChatMessage, NoticeMessage
from .ws_message import WSMessageBase
from ..base_model import ChzzkModel


class RecentChat(ChzzkModel):
    message_list: list[ChatMessage]
    user_count: Optional[int]
    notice: Optional[NoticeMessage]


class WSRecentChat(WSMessageBase):
    cmd: ChatCmd = ChatCmd.RECENT_CHAT
    ret_code: int
    ret_message: str = Field(alias='ret_msg')
    body: RecentChat = Field(alias='bdy')
