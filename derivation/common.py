from enum import Enum
from typing import TypeVar

__all__ = (
    "EventT",
    "FilterT",
    "PatternT",
    "ParamsMapT",
    "DerivationT",
)

EventT = TypeVar("EventT", bound=Enum)
FilterT = TypeVar("FilterT", bound=Enum)
PatternT = TypeVar("PatternT", bound=Enum)
ParamsMapT = TypeVar("ParamsMapT", bound=Enum)
DerivationT = TypeVar("DerivationT")
