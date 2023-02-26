from enum import Enum
from typing import Any, TypeVar

__all__ = (
    "EventT",
    "FilterT",
    "PatternT",
    "ParamsMapT",
    "DerivationT",
    "adapt_iterable",
)

EventT = TypeVar("EventT", bound=Enum)
FilterT = TypeVar("FilterT", bound=Enum)
PatternT = TypeVar("PatternT", bound=Enum)
ParamsMapT = TypeVar("ParamsMapT", bound=Enum)
DerivationT = TypeVar("DerivationT")


def adapt_iterable(param: Any) -> tuple:

    if isinstance(param, tuple):
        return param

    return (param,)
