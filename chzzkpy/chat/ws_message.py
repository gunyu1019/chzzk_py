from typing import Optional
from pydantic import Field

from .enums import ChatCmd
from ..base_model import ChzzkModel


class WSMessageBase(ChzzkModel):
    service_id: str = Field('game', alias='svcid')

    channel_id: str = Field(alias='cid')
    version: str = Field(alias='ver')
    tid: Optional[str]  # IDK: Full Name

    cmd: ChatCmd
