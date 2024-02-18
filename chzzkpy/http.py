from async_client_decorator import Session, get, Path
from typing import Annotated

from .live_status import LiveStatus


class ChzzkAPISession(Session):
    def __init__(self):
        super().__init__(base_url="https://api.chzzk.naver.com")

    @get("/polling/v2/channels/{channel_id}/")
    async def live_status(
            self,
            channel_id: Annotated[str, Path]
    ) -> LiveStatus:
        pass


class NaverGameAPISession(Session):
    def __init__(self):
        super().__init__(base_url="https://comm-api.game.naver.com")
