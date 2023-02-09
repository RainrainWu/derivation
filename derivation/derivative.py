from abc import ABC, abstractmethod
from collections import OrderedDict
from operator import __add__
from sys import intern
from typing import Callable, Generic, Iterable

from derivation.common import DerivationT, EventT
from derivation.constraint import AbstractConstrainable
from derivation.errors import ConstraintError, DerivativeError

__all__ = (
    "AbstractDerivable",
    "Derivative",
)


class AbstractDerivable(ABC, Generic[EventT, DerivationT]):

    __slots__ = ()

    @abstractmethod
    def validate(self, events: tuple[EventT, ...]) -> None:
        pass  # pragma: no cover

    @abstractmethod
    def derive(self, events: tuple[EventT, ...]) -> DerivationT:
        pass  # pragma: no cover

    @abstractmethod
    def exhaustive(self) -> Iterable[DerivationT]:
        pass  # pragma: no cover


class Derivative(AbstractDerivable, Generic[EventT, DerivationT]):

    __slots__ = (
        "__events",
        "__events_keys",
        "__events_count",
        "__func_derive",
        "__constraints",
    )

    ERR_MSG_EMPTY_DERIVE = intern("no events to be derived")

    def __init__(
        self,
        events: OrderedDict[EventT, DerivationT],
        func_derive: Callable[[DerivationT, DerivationT], DerivationT],
        /,
        constraints: Iterable[AbstractConstrainable] = (),
    ) -> None:

        self.__events = events
        self.__events_keys = tuple(self.__events.keys())
        self.__events_count = len(self.__events_keys)
        self.__func_derive = func_derive

        self.__constraints = constraints

    def validate(self, events: tuple[EventT, ...]) -> None:

        for constraint in self.__constraints:
            constraint.constrain(events)

    def derive(self, events: tuple[EventT, ...]) -> DerivationT:

        if not events:
            raise DerivativeError(self.ERR_MSG_EMPTY_DERIVE, {"events": events})

        self.validate(events)

        return self.__derive(events)

    def __derive(self, events: tuple[EventT, ...]) -> DerivationT:

        if len(events) == 1:
            return self.__events[events[0]]

        return self.__func_derive(self.__derive(events[:-1]), self.__events[events[-1]])

    def exhaustive(self) -> Iterable[tuple[tuple[EventT, ...], DerivationT]]:

        for order in self.__exhaustive(0, ()):
            try:
                self.validate(order)
                yield order, self.derive(order)
            except ConstraintError:
                continue

    def __exhaustive(
        self,
        pointer: int,
        order: tuple[EventT, ...],
    ) -> Iterable[tuple[EventT, ...]]:

        if pointer >= self.__events_count:

            if order:
                yield order

            return

        yield from self.__exhaustive(pointer + 1, (*order, self.__events_keys[pointer]))
        yield from self.__exhaustive(pointer + 1, order)
