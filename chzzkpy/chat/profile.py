from typing import Any, Optional
from pydantic import AliasChoices, computed_field, Field, PrivateAttr

from .enums import ChatType, UserRole
from ..base_model import ChzzkModel


class Badge(ChzzkModel):
    name: Optional[str]
    image_url: Optional[str]


class StreamingProperty(ChzzkModel):
    _following_dt: Optional[dict[str, str]] = PrivateAttr(default=None)
    _real_time_donation_ranking_dt: Optional[dict[str, str]] = PrivateAttr(default=None)

    def __init__(self, **kwargs):
        super(ChzzkModel, self).__init__(**kwargs)
        self._following_dt = kwargs.pop('following', None)
        self._real_time_donation_ranking_dt = kwargs.pop('realTimeDonationRanking', None)

    @computed_field
    @property
    def following_date(self) -> Optional[str]:
        if self._following_dt is None:
            return
        return self._following_dt['followDate']

    @computed_field
    @property
    def donation_ranking_badge(self) -> Optional[Badge]:
        if self._real_time_donation_ranking_dt is None or "badge" not in self._real_time_donation_ranking_dt.keys():
            return
        return Badge.model_validate_json(self._real_time_donation_ranking_dt["badge"])


class Profile(ChzzkModel):
    activity_badges: list[Any]
    user_id_hash: str
    user_role: UserRole = Field(alias='userRoleCode')
    nickname: str
    profile_image_url: Optional[str]
    _badge: Optional[dict[str, str]] = PrivateAttr(default=None)
    _title: Optional[dict[str, str]] = PrivateAttr(default=None)
    streaming_property: StreamingProperty
    verified_mark: bool

    def __init__(self, **kwargs):
        super(ChzzkModel, self).__init__(**kwargs)
        self._badge = kwargs.pop('badge', None)
        self._title = kwargs.pop('title', None)

    @computed_field
    @property
    def color(self) -> Optional[str]:
        if self._title is None:
            return
        return self._title['color']

    @computed_field
    @property
    def badge(self) -> Optional[Badge]:
        if self._badge is None and self._title is None:
            return
        _badge = self._badge or dict()
        _title = self._title or dict()
        return Badge(
            name=_title.get('name', None),
            image_url=_badge.get('imageUrl', None)
        )