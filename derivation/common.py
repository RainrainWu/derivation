from enum import Enum
from typing import TypeVar

EventT = TypeVar("EventT", bound=Enum)
FilterT = TypeVar("FilterT", bound=Enum)
PatternT = TypeVar("PatternT", bound=Enum)
DerivationT = TypeVar("DerivationT")
