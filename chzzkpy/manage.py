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

from typing import Optional, Union
from pydantic import BeforeValidator, Field

from .base_model import ChzzkModel


class ChatRule(ChzzkModel):
    channel_id: str
    rule: str


class ProhibitWord(ChzzkModel):
    created_date: datetime.datetime
    nickname: str
    prohibit_word: str
    prohibit_word_no: int


class Stream(ChzzkModel):
    stream_key: str
    stream_seq: int
    stream_url: str


class ChatAcitivityCount(ChzzkModel):
    chat_message_count: int
    restrict: bool
    restrict_count: int
    temporary_restrict: bool
    temporary_restrict_count: int
