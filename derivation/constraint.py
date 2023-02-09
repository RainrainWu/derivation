from abc import ABC, abstractmethod
from collections import Counter
from operator import itemgetter
from sys import intern
from typing import Generic, Iterable

from derivation.common import EventT
from derivation.errors import ConstraintError

__all__ = (
    "AbstractConstrainable",
    "MutuallyExclusiveConstraint",
    "OccurrenceConstraint",
    "PrerequisiteConstraint",
    "TerminationConstraint",
)


class AbstractConstrainable(ABC, Generic[EventT]):

    __slots__ = ()

    @abstractmethod
    def constrain(self, events: Iterable[EventT]) -> None:
        pass  # pragma: no cover


class MutuallyExclusiveConstraint(AbstractConstrainable, Generic[EventT]):

    __slots__ = ("__events_constrained",)

    ERR_MSG_EVENTS_CONFLICT = intern("mutually exclusive events conflict")

    def __init__(self, events_constrained: Iterable[EventT], /) -> None:

        self.__events_constrained = set(events_constrained)

    def constrain(self, events: Iterable[EventT], /) -> None:

        events_conflict = self.__events_constrained.intersection(set(events))
        if len(events_conflict) > 1:

            raise ConstraintError(
                self.ERR_MSG_EVENTS_CONFLICT,
                {"events_conflict": events_conflict},
            )


class OccurrenceConstraint(AbstractConstrainable, Generic[EventT]):

    __slots__ = (
        "__events_constrained",
        "__min_times",
        "__max_times",
    )

    ERR_MSG_OCCURRENCE_TIMES_OUT_OF_BOUND = intern("occurrence times out of bound")

    def __init__(
        self,
        events_constrained: Iterable[EventT],
        /,
        *,
        min_times: int = 0,
        max_times: int = 1,
    ) -> None:

        self.__events_constrained = set(events_constrained)

        self.__min_times = min_times
        self.__max_times = max_times

    def constrain(self, events: Iterable[EventT], /) -> None:

        events_counter = Counter(events)
        events_found = self.__events_constrained.intersection(set(events_counter))

        try:
            counts = itemgetter(*events_found)(events_counter)
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


class PrerequisiteConstraint(AbstractConstrainable, Generic[EventT]):

    __slots__ = (
        "__events_prerequisite",
        "__events_subsequent",
    )

    ERR_MSG_EVENTS_NOT_SPECIFIED = intern("prerequisite or subsequent not specified")
    ERR_MSG_INVALID_OVERLAP = intern(
        "invalid overlap between prerequisite and subsequent"
    )
    ERR_MSG_FAILED_PREREQUISITE = intern("failed to satisfied with prerequisite")
    ERR_MSG_PREREQUISITE_NOT_FOUND = intern("prerequisite not found")

    def __init__(
        self,
        events_prerequisite: Iterable[EventT],
        events_subsequent: Iterable[EventT],
        /,
    ) -> None:

        self.__events_prerequisite = set(events_prerequisite)
        self.__events_subsequent = set(events_subsequent)

        if not self.__events_prerequisite or not self.__events_subsequent:
            raise ConstraintError(
                self.ERR_MSG_EVENTS_NOT_SPECIFIED,
                {
                    "prerequisite": self.__events_prerequisite,
                    "subsequent": self.__events_subsequent,
                },
            )

        if overlap := self.__events_prerequisite.intersection(self.__events_subsequent):

            raise ConstraintError(
                self.ERR_MSG_INVALID_OVERLAP,
                {"overlap": overlap},
            )

    def constrain(self, events: Iterable[EventT], /) -> None:

        indexes_subsequent = set()
        for layer in self.__events_subsequent:
            indexes_subsequent |= set(
                [idx for idx, val in enumerate(events) if val == layer]
            )

        if not indexes_subsequent:
            return

        indexes_prerequisite = set()
        for layer in self.__events_prerequisite:
            indexes_prerequisite |= set(
                [idx for idx, val in enumerate(events) if val == layer]
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


class TerminationConstraint(AbstractConstrainable, Generic[EventT]):

    __slots__ = ("__terminations",)

    ERR_MSG_INVALID_TERMINATION = "invalid termination within given events"
    ERR_MSG_NO_EVENTS_PROVIDED = "no events provided"

    def __init__(self, terminations: set[EventT], /) -> None:

        self.__terminations = terminations

    def constrain(self, events: Iterable[EventT], /) -> None:

        try:

            if (termination := tuple(events)[-1]) not in self.__terminations:
                raise ConstraintError(
                    self.ERR_MSG_INVALID_TERMINATION,
                    {"termination_given": termination},
                )

        except IndexError:
            raise ConstraintError(self.ERR_MSG_NO_EVENTS_PROVIDED)
