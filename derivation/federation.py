from abc import ABC, abstractmethod
from functools import reduce
from inspect import signature
from operator import itemgetter, or_
from sys import intern
from typing import Any, Callable, Generic, Iterable

from derivation.common import DerivationT, FilterT, ParamsMapT, PatternT
from derivation.derivative import Derivative
from derivation.errors import FederationError

__all__ = (
    "AbstractFederative",
    "Federation",
)


class AbstractFederative(ABC, Generic[PatternT, ParamsMapT, FilterT, DerivationT]):

    __slots__ = ()

    @abstractmethod
    def exhaustive(
        self,
        pattern: PatternT,
        /,
        params_maps: tuple[ParamsMapT, ...] = (),
        params_customize: dict[str, Any] = {},
        filters_applied: tuple[FilterT, ...] = (),
    ) -> Iterable[DerivationT]:
        pass  # pragma: no cover


class Federation(
    AbstractFederative, Generic[PatternT, ParamsMapT, FilterT, DerivationT]
):

    __slots__ = (
        "__derivatives",
        "__patterns",
        "__params_maps",
        "__filters",
    )

    ERR_MSG_PATTERN_NOT_FOUND = intern("pattern not found")

    def __init__(
        self,
        derivatives: dict[str, Derivative],
        patterns: dict[PatternT, Callable[..., DerivationT]],
        /,
        params_maps: dict[ParamsMapT, dict[str, Any]] = {},
        filters: dict[FilterT, Callable[[DerivationT], bool]] = {},
    ) -> None:

        self.__derivatives = derivatives
        self.__patterns = patterns
        self.__params_maps = params_maps
        self.__filters = filters

    def __collect_params(
        self,
        params_maps: tuple[ParamsMapT, ...] = (),
        params_customized: dict[str, Any] = {},
    ) -> dict[str, Any]:

        if not params_maps:
            return {}

        if len(params_maps) == 1:
            return self.__params_maps[params_maps[0]] | params_customized

        return (
            dict(
                reduce(
                    or_,
                    itemgetter(*params_maps)(self.__params_maps),
                )
            )
            | params_customized
        )

    def __get_filtered_candidates(
        self,
        /,
        func_federate: Callable[..., DerivationT],
        params_mapped: dict[str, Any],
        filters_applied: tuple[FilterT, ...] = (),
    ) -> Iterable[DerivationT]:

        params_federated = tuple(signature(func_federate).parameters.keys())
        params_desired = tuple(
            param for param in params_federated if param not in params_mapped
        )
        for params_group in self.__exhaustive(params_desired, {}):

            candidate = func_federate(**(params_group | params_mapped))
            try:
                for filter_applied in filters_applied:
                    if not self.__filters[filter_applied](candidate):
                        raise ValueError
            except ValueError:
                continue
            else:
                yield candidate

    def exhaustive(
        self,
        pattern: PatternT,
        /,
        params_maps: tuple[ParamsMapT, ...] = (),
        params_customize: dict[str, Any] = {},
        filters_applied: tuple[FilterT, ...] = (),
    ) -> Iterable[DerivationT]:

        try:
            func_federate = self.__patterns[pattern]
        except KeyError:
            raise FederationError(
                self.ERR_MSG_PATTERN_NOT_FOUND,
                {"pattern": pattern},
            )

        params_desired = signature(func_federate).parameters.keys()
        params_mapped = self.__collect_params(params_maps, params_customize)
        params_derived = self.__derivatives.keys()

        if set(params_desired) - (set(params_mapped) | set(params_derived)):
            raise FederationError

        yield from self.__get_filtered_candidates(
            func_federate,
            params_mapped,
            filters_applied,
        )

    def __exhaustive(
        self,
        params_desired: tuple[str, ...],
        params: dict[str, Any],
    ) -> Iterable[dict[str, Any]]:

        if len(params_desired) == len(params):
            yield params
            return

        param_picked = params_desired[len(params)]
        for _, candidate in self.__derivatives[param_picked].exhaustive():
            yield from self.__exhaustive(
                params_desired,
                params | {param_picked: candidate},
            )
