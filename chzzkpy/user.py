import datetime
from typing import Annotated, Any

from pydantic import BeforeValidator

from .base_model import ChzzkModel


class User(ChzzkModel):
    has_profile: bool
    user_id_hash: str | None
    nickname: str | None
    profile_image_url: str | None
    penalties: list[Any] | None  # typing: ???
    official_noti_agree: bool
    official_noti_agree_updated_date: Annotated[
        datetime.datetime | None,
        BeforeValidator(
            ChzzkModel.special_date_parsing_validator
        )
    ]  # Example: YYYY-MM-DDTHH:MM:SS.SSS+09
    verified_mark: bool
    logged_in: bool | None
