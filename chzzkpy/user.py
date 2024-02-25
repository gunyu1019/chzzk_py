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
        BeforeValidator(ChzzkModel.special_date_parsing_validator),
    ]  # Example: YYYY-MM-DDTHH:MM:SS.SSS+09
    verified_mark: bool
    logged_in: Optional[bool]
