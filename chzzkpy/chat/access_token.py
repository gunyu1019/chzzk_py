from ..base_model import ChzzkModel


class TemporaryRestrict(ChzzkModel):
    temporary_restrict: bool
    times: int
    duration: int | None
    created_time: int | None


class AccessToken(ChzzkModel):
    access_token: str
    temporary_restrict: TemporaryRestrict
    real_name_auth: bool
    extra_token: str
