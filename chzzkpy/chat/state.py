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

import inspect
import functools
from typing import Callable, Any

from .blind import Blind
from .enums import ChatCmd, ChatType, get_enum
from .message import ChatMessage, DonationMessage, NoticeMessage, SystemMessage
from .recent_chat import RecentChat


class ConnectionState:
    def __init__(
        self,
        dispatch: Callable[..., Any],
        handler: dict[ChatCmd | int, Callable[..., Any]],
    ):
        self.dispatch = dispatch
        self.handler: dict[ChatCmd | int, Callable[..., Any]] = handler
        self.parsers: dict[ChatCmd, Callable[..., Any]] = dict()
        for _, func in inspect.getmembers(self):
            if hasattr(func, "__parsing_event__"):
                self.parsers[func.__parsing_event__] = func

    @staticmethod
    def parsable(cmd: ChatCmd):
        def decorator(func: Callable[..., Any]):
            func.__parsing_event__ = cmd
            return func

        return decorator

    @staticmethod
    def catch_exception(func: Callable[..., Any]):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as exc:
                self.dispatch("client_error", exc, *args, **kwargs)

        return wrapper

    def call_handler(self, key: ChatCmd, *args: Any, **kwargs: Any):
        if key in self.handler:
            func = self.handler[key]
            func(*args, **kwargs)

    @parsable(ChatCmd.CONNECTED)
    @catch_exception
    def parse_connect(self, _: dict[str, Any]):
        self.call_handler(ChatCmd.CONNECTED)
        self.dispatch("connect")

    def _parse_all_type_of_chat(self, data: list[dict[str, Any]]):
        if data is None or len(data) == 0:
            return

        for message in data:
            message_raw_type = message.get("messageTypeCode") or message.get(
                "msgTypeCode"
            )
            message_type = get_enum(ChatType, message_raw_type)

            # Cause bug from insufficient information
            # ChatType: SYSTEM_MESSAGE
            if message.get("profile") == "{}":
                message["profile"] = None

            if message_type == ChatType.DONATION:
                validated_data = DonationMessage.model_validate(message)
                self.dispatch("donation", validated_data)
            elif message_type == ChatType.SYSTEM_MESSAGE:

                validated_data = SystemMessage.model_validate(message)
                self.dispatch("system_message", validated_data)
            elif message_type == ChatType.TEXT:
                validated_data = ChatMessage.model_validate(message)
                self.dispatch("chat", validated_data)

    @parsable(ChatCmd.CHAT)
    @catch_exception
    def parse_chat(self, data: list[dict[str, Any]]):
        self._parse_all_type_of_chat(data)

    @parsable(ChatCmd.RECENT_CHAT)
    @catch_exception
    def parse_recent_chat(self, data: dict[str, Any]):
        validated_data = RecentChat.model_validate(data)
        self.dispatch("recent_chat", validated_data)

    @parsable(ChatCmd.SPECIAL_CHAT)
    @catch_exception
    def parse_special_chat(self, data: list[dict[str, Any]]):
        self._parse_all_type_of_chat(data)

    @parsable(ChatCmd.NOTICE)
    @catch_exception
    def parse_notice(self, data: dict[str, Any]):
        if not data:
            self.dispatch("unpin")
        validated_data = NoticeMessage.model_validate(data)
        self.dispatch("notice", validated_data)
        self.dispatch("pin", validated_data)

    @parsable(ChatCmd.BLIND)
    @catch_exception
    def parse_blind(self, data: dict[str, Any]):
        validated_data = Blind.model_validate(data)
        self.dispatch("blind", validated_data)
