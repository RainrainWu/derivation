from abc import ABC, abstractmethod
from collections import Counter
from operator import itemgetter
from sys import intern
from typing import Generic, Iterable

from derivation.errors import ConstraintError
from derivation.types import VariantLayerT


class AbstractConstrainable(ABC, Generic[VariantLayerT]):
    @abstractmethod
    def constrain(self, event_labels: tuple[VariantLayerT, ...]) -> None:
        pass  # pragma: no cover


class MutuallyExclusiveConstraint(AbstractConstrainable):

    ERR_MSG_LAYERS_CONFLICT = intern("mutually exclusive layers conflict")

    def __init__(self, layers_constrained: Iterable[VariantLayerT], /) -> None:

        self.__layers_constrained = set(layers_constrained)

    def constrain(self, layers: Iterable[VariantLayerT], /) -> None:

        layers_conflict = self.__layers_constrained.intersection(set(layers))
        if len(layers_conflict) > 1:

            raise ConstraintError(
                self.ERR_MSG_LAYERS_CONFLICT,
                {"conflict_layers": layers_conflict},
            )


class OccurrenceConstraint(AbstractConstrainable):

    ERR_MSG_OCCURRENCE_TIMES_OUT_OF_BOUND = intern("occurrence times out of bound")

    def __init__(
        self,
        layers_constrained: Iterable[VariantLayerT],
        /,
        *,
        min_times: int = 0,
        max_times: int = 1,
    ) -> None:

        self.__layers_constrained = set(layers_constrained)

        self.__min_times = min_times
        self.__max_times = max_times

    def constrain(self, layers: Iterable[VariantLayerT], /) -> None:

        layers_counter = Counter(layers)
        layers_found = self.__layers_constrained.intersection(set(layers_counter))

        try:
            counts = itemgetter(*layers_found)(layers_counter)
            occurrence = counts if isinstance(counts, int) else sum(counts)
        except TypeError:
            occurrence = 0

        if not (self.__min_times <= occurrence <= self.__max_times):
            raise ConstraintError(
                self.ERR_MSG_OCCURRENCE_TIMES_OUT_OF_BOUND,
                {
                    "min_times": self.__min_times,
                    "max_times": self.__max_times,
                    "occurrence": occurrence,
                },
            )


class PrerequisiteConstraint(AbstractConstrainable):

    ERR_MSG_LAYERS_NOT_SPECIFIED = intern("prerequisite or subsequent not specified")
    ERR_MSG_INVALID_OVERLAP = intern(
        "invalid overlap between prerequisite and subsequent"
    )
    ERR_MSG_FAILED_PREREQUISITE = intern("failed to satisfied with prerequisite")
    ERR_MSG_PREREQUISITE_NOT_FOUND = intern("prerequisite not found")

    def __init__(
        self,
        layers_prerequisite: Iterable[VariantLayerT],
        layers_subsequent: Iterable[VariantLayerT],
        /,
    ) -> None:

        self.__layers_prerequisite = set(layers_prerequisite)
        self.__layers_subsequent = set(layers_subsequent)

        if not self.__layers_prerequisite or not self.__layers_subsequent:
            raise ConstraintError(
                self.ERR_MSG_LAYERS_NOT_SPECIFIED,
                {
                    "prerequisite": self.__layers_prerequisite,
                    "subsequent": self.__layers_subsequent,
                },
            )

        if overlap := self.__layers_prerequisite.intersection(self.__layers_subsequent):

            raise ConstraintError(
                self.ERR_MSG_INVALID_OVERLAP,
                {"overlap": overlap},
            )

    def constrain(self, layers: Iterable[VariantLayerT], /) -> None:

        indexes_subsequent = set()
        for layer in self.__layers_subsequent:
            indexes_subsequent |= set(
                [idx for idx, val in enumerate(layers) if val == layer]
            )

        if not indexes_subsequent:
            return

        indexes_prerequisite = set()
        for layer in self.__layers_prerequisite:
            indexes_prerequisite |= set(
                [idx for idx, val in enumerate(layers) if val == layer]
            )

        if not indexes_prerequisite:
            raise ConstraintError(
                self.ERR_MSG_PREREQUISITE_NOT_FOUND,
            )

        if max(indexes_prerequisite) >= min(indexes_subsequent):
            raise ConstraintError(
                self.ERR_MSG_FAILED_PREREQUISITE,
                {
                    "last_prerequisite_index": max(indexes_prerequisite),
                    "first_subsequent_index": min(indexes_subsequent),
                },
            )
