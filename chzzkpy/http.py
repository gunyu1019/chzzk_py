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

import asyncio
import functools
import inspect
import logging
from typing import Annotated, Optional

import aiohttp
from async_client_decorator import Session, get, Path

from .base_model import ChzzkModel, Content
from .error import LoginRequired
from .live import LiveStatus, LiveDetail
from .user import User

_log = logging.getLogger(__name__)


# This decorator will remove at https://github.com/gunyu1019/async-client-decorator/issues/8
def _response_pydantic_model_validation(func):
    signature = inspect.signature(func)
    if not issubclass(signature.return_annotation, ChzzkModel):
        return func

    signature = inspect.signature(func)

    @functools.wraps(func)
    async def wrapper(self: Session, response: aiohttp.ClientResponse, *_1, **_2):
        data = await response.json()
        validated_data = signature.return_annotation.model_validate(data)
        return validated_data

    return wrapper


# This decorator will remove at https://github.com/gunyu1019/async-client-decorator/issues/8
def _response_pydantic_model_validation_able(func):
    signature = inspect.signature(func)
    if not issubclass(signature.return_annotation, ChzzkModel):
        return func

    func.__component_parameter__.response.append("response")
    return func


# This decorator will remove at https://github.com/gunyu1019/async-client-decorator/issues/9
def _custom_query_name(oldest_name, replace_name):
    def decorator(func):
        func.__component_parameter__.query[replace_name] = (
            func.__component_parameter__.query.pop(oldest_name)
        )

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            kwargs[replace_name] = kwargs.pop(oldest_name)
            return func(self, *args, **kwargs)

        return wrapper

    return decorator


class ChzzkSession(Session):
    def __init__(self, base_url: str, loop: Optional[asyncio.AbstractEventLoop] = None):
        super().__init__(base_url=base_url, loop=loop)

        self._authorization_key = None
        self._session_key = None

    def login(self, authorization_key: str, session_key: str):
        self._authorization_key = authorization_key
        self._session_key = session_key

    @property
    def has_login(self) -> bool:
        return self._authorization_key is not None and self._session_key is not None

    @staticmethod
    def login_required(func):
        @functools.wraps(func)
        async def wrapper(self: "ChzzkSession", *args, **kwargs):
            if not self.has_login:
                raise LoginRequired()

            return await func(self, *args, **kwargs)

        return wrapper

    @staticmethod
    def login_able(func):
        @functools.wraps(func)
        async def wrapper(self: "ChzzkSession", *args, **kwargs):
            if self.has_login:
                if "Cookie" not in func.__component_parameter__.header.keys():
                    func.__component_parameter__.header["Cookie"] = ""
                func.__component_parameter__.header["Cookie"] += self._token
            return await func(self, *args, **kwargs)

        return wrapper

    @staticmethod
    def logging(func):
        @functools.wraps(func)
        def wrapper(self: "ChzzkSession", *args, **kwargs):
            _log.debug(f"Path({func.__request_path__}) was called.")
            return func(self, *args, **kwargs)

        return wrapper

    @property
    def _token(self) -> str:
        return f"NID_SES={self._session_key}; NID_AUT={self._authorization_key}"


class ChzzkAPISession(ChzzkSession):
    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None):
        super().__init__(base_url="https://api.chzzk.naver.com", loop=loop)

    @_response_pydantic_model_validation_able
    @ChzzkSession.logging
    @get("/polling/v2/channels/{channel_id}/live-status")
    @_response_pydantic_model_validation
    async def live_status(
        self, channel_id: Annotated[str, Path]
    ) -> Content[LiveStatus]:
        pass

    @_response_pydantic_model_validation_able
    @ChzzkSession.logging
    @get("/service/v2/channels/{channel_id}/live-detail")
    @_response_pydantic_model_validation
    async def live_detail(
        self, channel_id: Annotated[str, Path]
    ) -> Content[LiveDetail]:
        pass


class NaverGameAPISession(ChzzkSession):
    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None):
        super().__init__(base_url="https://comm-api.game.naver.com", loop=loop)

    @_response_pydantic_model_validation_able
    @ChzzkSession.logging
    @ChzzkSession.login_required
    @ChzzkSession.login_able
    @get("/nng_main/v1/user/getUserStatus")
    @_response_pydantic_model_validation
    async def user(self) -> Content[User]:
        pass
