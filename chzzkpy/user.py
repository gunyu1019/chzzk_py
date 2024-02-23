import datetime
from typing import Annotated, Any, Optional

from pydantic import BeforeValidator

from .base_model import ChzzkModel


class User(ChzzkModel):
    has_profile: bool
    user_id_hash: Optional[str]
    nickname: Optional[str]
    profile_image_url: Optional[str]
    penalties: Optional[list[Any]]  # typing: ???
    official_noti_agree: bool
    official_noti_agree_updated_date: Annotated[
        Optional[datetime.datetime],
        BeforeValidator(
            ChzzkModel.special_date_parsing_validator
        )
    ]  # Example: YYYY-MM-DDTHH:MM:SS.SSS+09
    verified_mark: bool
    logged_in: Optional[bool]
