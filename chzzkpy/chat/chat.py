from pydantic import Field

from .enums import ChatCmd
from .message import ChatMessage
from .ws_message import WSMessageBase


class WSMessageChat(WSMessageBase):
    cmd: ChatCmd = ChatCmd.CHAT
    body: list[ChatMessage] = Field(alias='bdy')
