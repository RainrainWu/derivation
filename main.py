from enum import Enum, auto
from operator import or_

from derivation.constraint import (
    MutuallyExclusiveConstraint,
    OccurrenceConstraint,
    PrerequisiteConstraint,
    TerminationConstraint,
)
from derivation.derivative import Derivative


class DerivativeEvent(Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.upper()


class DerivativeEventAlpha(DerivativeEvent):

    ESSENTIALS = auto()

    OPTIONAL_1 = auto()
    OPTIONAL_1_1 = auto()
    OPTIONAL_1_2 = auto()

    OPTIONAL_2 = auto()
    OPTIONAL_3 = auto()


EVENT_ALPHA = {event: {event.value: None} for event in DerivativeEventAlpha}

derivative = Derivative(
    EVENT_ALPHA,
    or_,
    (
        OccurrenceConstraint(
            (DerivativeEventAlpha.ESSENTIALS,),
            min_times=1,
            max_times=1,
        ),
        MutuallyExclusiveConstraint(
            (
                DerivativeEventAlpha.OPTIONAL_1,
                DerivativeEventAlpha.OPTIONAL_2,
                DerivativeEventAlpha.OPTIONAL_3,
            ),
        ),
        MutuallyExclusiveConstraint(
            (DerivativeEventAlpha.OPTIONAL_1_1, DerivativeEventAlpha.OPTIONAL_1_2),
        ),
        PrerequisiteConstraint(
            (DerivativeEventAlpha.OPTIONAL_1,),
            (DerivativeEventAlpha.OPTIONAL_1_1, DerivativeEventAlpha.OPTIONAL_1_2),
        ),
        TerminationConstraint(
            {
                DerivativeEventAlpha.OPTIONAL_1_1,
                DerivativeEventAlpha.OPTIONAL_1_2,
                DerivativeEventAlpha.OPTIONAL_2,
                DerivativeEventAlpha.OPTIONAL_3,
            },
        ),
    ),
)

for order, result in derivative.exhaustive():

    print(f"{order}\n{result}\n")
