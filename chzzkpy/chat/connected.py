from typing import Literal, Optional
from pydantic import Field

from .enums import ChatCmd
from .ws_message import WSMessageBase
from ..base_model import ChzzkModel


class ConnectedInfo(ChzzkModel):
    access_token: str = Field(alias='accTkn')
    auth: Literal['SEND', 'READ']
    uuid: Optional[str]
    session_id: str = Field(alias='sid')


class WSMessageConnected(WSMessageBase):
    cmd: ChatCmd = ChatCmd.CONNECTED
    ret_code: int
    ret_message: str = Field(alias='ret_msg')
    body: ConnectedInfo
