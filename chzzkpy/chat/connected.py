from typing import Literal, Optional

from pydantic import Field

from ..base_model import ChzzkModel


class ConnectedInfo(ChzzkModel):
    access_token: str = Field(alias="accTkn")
    auth: Literal["SEND", "READ"]
    uuid: Optional[str]
    session_id: str = Field(alias="sid")
