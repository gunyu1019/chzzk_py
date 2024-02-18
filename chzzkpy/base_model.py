from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

T = TypeVar('T')


class ChzzkModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
    )


class Content(ChzzkModel, Generic[T]):
    code: int
    message: str | None
    content: T
