from typing import Optional

from .message import ChatMessage, NoticeMessage
from ..base_model import ChzzkModel


class RecentChat(ChzzkModel):
    message_list: list[ChatMessage]
    user_count: Optional[int]
    notice: Optional[NoticeMessage]
