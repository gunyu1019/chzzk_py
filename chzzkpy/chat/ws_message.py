from pydantic import Field

from .enums import ChatCmd
from ..base_model import ChzzkModel


class WSMessageBase(ChzzkModel):
    svcid: str = 'game'

    channel_id: str = Field(alias='cid')
    version: str = Field('ver')
    tid: str

    cmd: ChatCmd
