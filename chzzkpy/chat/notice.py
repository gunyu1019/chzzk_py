from pydantic import Field

from .enums import ChatCmd
from .message import NoticeMessage
from .ws_message import WSMessageBase


class WSNotice(WSMessageBase):
    cmd: ChatCmd = ChatCmd.NOTICE
    body: NoticeMessage = Field(alias='bdy')
