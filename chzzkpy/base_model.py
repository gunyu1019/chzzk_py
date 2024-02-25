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
    content: T
