"""MIT License

Copyright (c) 2024 gunyu1019

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import annotations

from typing import Optional, Literal
from pydantic import AliasChoices, Field

from ..base_model import ChzzkModel


class DonationRank(ChzzkModel):
    user_id_hash: str
    nickname: str = Field(validation_alias=AliasChoices("nickname", "nickName"))
    verified_mark: bool
    donation_amount: int
    ranking: int


class BaseDonation(ChzzkModel):
    is_anonymous: bool = True
    pay_type: str
    pay_amount: int = 0
    donation_type: str
    weekly_rank_list: Optional[list[DonationRank]] = Field(default_factory=list)
    donation_user_weekly_rank: Optional[DonationRank] = None


class ChatDonation(BaseDonation):
    donation_type: Literal["CHAT"]


class VideoDonation(BaseDonation):
    donation_type: Literal["VIDEO"]


class MissionDonation(BaseDonation):
    donation_type: Literal["MISSION"]
    duration_time: Optional[int] = None
    mission_donation_id: Optional[str] = None
    mission_created_time: Optional[str] = None
    mission_end_time: Optional[str] = None
    mission_text: Optional[str] = None

    status: Optional[str] = None  # PENDING / REJECTED / ALLOW
    success: Optional[bool] = None