from abc import ABC, abstractmethod
from enum import Enum
from inspect import signature
from sys import intern
from typing import Any, Callable, Generic, Iterable

from derivation.common import DerivationT, FilterT, PatternT
from derivation.derivative import Derivative, d1, d2
from derivation.errors import FederationError


class AbstractFederative(ABC, Generic[PatternT, FilterT, DerivationT]):

    __slots__ = ()

    @abstractmethod
    def exhaustive(
        self,
        pattern: PatternT,
        filters_applied: tuple[FilterT, ...],
    ) -> Iterable[DerivationT]:
        pass  # pragma: no cover


class Federation(AbstractFederative, Generic[PatternT, FilterT, DerivationT]):

    __slots__ = (
        "__derivatives",
        "__patterns",
        "__filters",
    )

    ERR_MSG_PATTERN_NOT_FOUND = intern("pattern not found")

    def __init__(
        self,
        derivatives: dict[str, Derivative],
        patterns: dict[PatternT, Callable[..., DerivationT]],
        /,
        filters: dict[FilterT, Callable[[DerivationT], bool]] = {},
    ) -> None:

        self.__derivatives = derivatives
        self.__patterns = patterns
        self.__filters = filters

    def exhaustive(
        self,
        pattern: PatternT,
        filters_applied: tuple[FilterT, ...] = (),
    ) -> Iterable[DerivationT]:

        try:
            func_federate = self.__patterns[pattern]
        except KeyError:
            raise FederationError(
                self.ERR_MSG_PATTERN_NOT_FOUND,
                {"pattern": pattern},
            )

        params_desired = set(signature(func_federate).parameters.keys())
        params_registered = set(self.__derivatives.keys())

        if params_desired - params_registered:
            raise FederationError

        for candidate in self.__exhaustive(func_federate, {}):

            try:
                for filter_applied in filters_applied:
                    if not self.__filters[filter_applied](candidate):
                        raise ValueError
            except ValueError:
                continue
            else:
                yield candidate

    def __exhaustive(
        self,
        func_federate: Callable[..., DerivationT],
        params: dict[str, Any],
    ) -> Iterable[DerivationT]:

        params_desired = tuple(signature(func_federate).parameters.keys())
        if len(params_desired) == len(params):
            yield func_federate(**params)
            return

        param_pick = params_desired[len(params)]
        for _, candidate in self.__derivatives[param_pick].exhaustive():
            yield from self.__exhaustive(
                func_federate,
                params | {param_pick: candidate},
            )
