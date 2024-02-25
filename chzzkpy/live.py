import datetime
from typing import Literal, Any, Optional
from pydantic import Field, Json
from .base_model import ChzzkModel


class LivePollingStatus(ChzzkModel):
    status: str
    is_publishing: bool
    playable_status: str
    traffic_throttling: int
    call_period_millisecond: int = Field(alias="callPeriodMilliSecond")


class LiveStatus(ChzzkModel):
    live_title: str
    status: Literal["OPEN", "CLOSE"]
    concurrent_user_count: int
    accumulate_count: int
    paid_promotion: bool
    adult: bool
    chat_channel_id: str
    category_type: Optional[str]
    live_category: str
    live_category_value: str
    live_polling_status: Json[LivePollingStatus] = Field(alias="livePollingStatusJson")
    fault_status: Any  # typing: ???
    user_adult_status: str
    chat_active: bool
    chat_available_group: str
    chat_available_condition: str
    min_follower_minute: int


class LiveDetail(ChzzkModel):
    live_id: int
    live_title: str
    status: Literal["OPEN", "CLOSE"]
    live_image_url: str
    default_thumbnail_image_url: Optional[str]
    concurrent_user_count: int
    accumulate_count: int
    open_date: datetime.datetime
    close_date: datetime.datetime
    adult: bool
    chat_channel_id: str
    category_type: Optional[str]
    live_category: str
    live_category_value: str
    chat_active: bool
    chat_available_group: str
    chat_available_condition: str
    paid_promotion: bool
    min_follower_minute: int
    user_adult_status: Optional[str]

    # live_playback: Json[LivePlayback] = Field(alias="livePlaybackJson") WIP
    live_polling_status: Json[LivePollingStatus] = Field(alias="livePollingStatusJson")
