# Derivation

[![Maintainability](https://api.codeclimate.com/v1/badges/08e384eaba6ad7375e8b/maintainability)](https://codeclimate.com/github/RainrainWu/derivation/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/08e384eaba6ad7375e8b/test_coverage)](https://codeclimate.com/github/RainrainWu/derivation/test_coverage)
[![codecov](https://codecov.io/gh/RainrainWu/derivation/branch/master/graph/badge.svg?token=at8Ckp5iLi)](https://codecov.io/gh/RainrainWu/derivation)
[![Github Actions](https://github.com/RainrainWu/derivation/actions/workflows/pull_request.yml/badge.svg)](https://github.com/RainrainWu/derivation/actions/workflows/pull_request.yml)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/derivation.svg)](https://pypi.python.org/pypi/derivation/)

Derivation is a flexible payload generating framework with highly-customizable patterns and rules which raise your efficiency significantly on test case implementation against complicated inputs.

## Getting Started

### Derivative

Derivative is the primary object which sorted out all of valid outputs meet the constraints.

> The script below can be executed directly
```python
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
```