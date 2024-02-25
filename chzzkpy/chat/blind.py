import datetime
from typing import Optional
from pydantic import Field

from ..base_model import ChzzkModel


class Blind(ChzzkModel):
    service_id: str
    time: datetime.datetime = Field(alias="messageTime")
    blind_type: str
    blind_user_id: Optional[str]
    user_id: str
    message: Optional[str]
