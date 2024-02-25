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

from typing import Optional, Self
from types import TracebackType
from .http import ChzzkAPISession, NaverGameAPISession
from .live import LiveStatus, LiveDetail
from .user import User


class Client:
    def __init__(
        self,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        authorization_key: Optional[str] = None,
        session_key: Optional[str] = None,
    ):
        self.loop = loop or asyncio.get_event_loop()
        self._api_session = ChzzkAPISession(loop=loop)
        self._game_session = NaverGameAPISession(loop=loop)
        self._closed = False

        if authorization_key is not None and session_key is not None:
            self.login(authorization_key, session_key)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        if not self.is_closed:
            await self.close()

    @property
    def is_closed(self) -> bool:
        return self._closed

    async def close(self):
        self._closed = True
        await self._api_session.close()
        await self._game_session.close()
        return

    def login(self, authorization_key: str, session_key: str):
        self._api_session.login(authorization_key, session_key)
        self._game_session.login(authorization_key, session_key)

    async def live_status(self, channel_id: str) -> LiveStatus:
        res = await self._api_session.live_status(channel_id=channel_id)
        return res.content

    async def live_detail(self, channel_id: str) -> LiveDetail:
        res = await self._api_session.live_detail(channel_id=channel_id)
        return res.content

    async def user(self) -> User:
        res = await self._game_session.user()
        return res.content
