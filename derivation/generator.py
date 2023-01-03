from functools import lru_cache
from sys import intern
from typing import Callable, Generic, Iterable

from derivation.constraint import AbstractConstrainable
from derivation.errors import GeneratorError
from derivation.types import VariantLayerT, VariantT


class DerivationGenerator(Generic[VariantLayerT, VariantT]):

    ERR_MSG_NO_LAYERS_TO_BE_ACCUMULATED = intern("no layers to be accumulated")

    def __init__(
        self,
        layers: dict[VariantLayerT, VariantT],
        func_accumulate: Callable[[VariantT, VariantT], VariantT],
        /,
        constraints: Iterable[AbstractConstrainable] = (),
    ) -> None:

        self.__layers = layers
        self.__func_accumulate = func_accumulate

        self.__constraints = constraints

    def validate(self, layers: Iterable[VariantLayerT]) -> None:

        for constraint in self.__constraints:
            constraint.constrain(layers)

    def accumulate(self, layers: Iterable[VariantLayerT]) -> VariantT:

        if not layers:
            raise GeneratorError(
                self.ERR_MSG_NO_LAYERS_TO_BE_ACCUMULATED,
                {"layers": layers},
            )

        self.validate(layers)

        return self.__accumulate(layers)

    @lru_cache(maxsize=None)
    def __accumulate(self, layers: Iterable[VariantLayerT]) -> VariantT:

        if len(layers) == 1:
            return self.__layers[layers[0]]

        return self.__func_accumulate(
            self.__accumulate(layers[:-1]), self.__layers[layers[-1]]
        )
