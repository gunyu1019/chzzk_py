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

from typing import Generic, TypeVar, Optional

from pydantic import BaseModel, ConfigDict, Extra
from pydantic.alias_generators import to_camel

T = TypeVar("T")


class ChzzkModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel, frozen=True, extra=Extra.allow  # prevent exception.
    )

    @staticmethod
    def special_date_parsing_validator(value: T) -> T:
        if not isinstance(value, str):
            return value
        return value.replace("+09", "")


class Content(ChzzkModel, Generic[T]):
    code: int
    message: Optional[str]
    content: Optional[T]
