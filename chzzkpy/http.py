import functools
import inspect

import aiohttp
from async_client_decorator import Session, get, Path
from typing import Annotated

from .base_model import ChzzkModel, Content
from .live_status import LiveStatus, LiveDetail


def _response_pydantic_model_validation(func):
    signature = inspect.signature(func)
    if not issubclass(signature.return_annotation, ChzzkModel):
        return func

    signature = inspect.signature(func)

    @functools.wraps(func)
    async def wrapper(self, response: aiohttp.ClientResponse, *_1, **_2):
        data = await response.json()
        validated_data = signature.return_annotation.model_validate(data)
        return validated_data
    return wrapper


def _response_pydantic_model_validation_able(func):
    signature = inspect.signature(func)
    if not issubclass(signature.return_annotation, ChzzkModel):
        return func

    func.__component_parameter__.response.append("response")
    return func


class ChzzkAPISession(Session):
    def __init__(self):
        super().__init__(base_url="https://api.chzzk.naver.com")

    @_response_pydantic_model_validation_able
    @get("/polling/v2/channels/{channel_id}/live-status")
    @_response_pydantic_model_validation
    async def live_status(
            self,
            channel_id: Annotated[str, Path]
    ) -> Content[LiveStatus]:
        pass

    @_response_pydantic_model_validation_able
    @get("/service/v2/channels/{channel_id}/live-detail")
    @_response_pydantic_model_validation
    async def live_detail(
            self,
            channel_id: Annotated[str, Path]
    ) -> Content[LiveDetail]:
        pass



class NaverGameAPISession(Session):
    def __init__(self):
        super().__init__(base_url="https://comm-api.game.naver.com")
