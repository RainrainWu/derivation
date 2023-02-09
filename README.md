# Derivation

[![Maintainability](https://api.codeclimate.com/v1/badges/08e384eaba6ad7375e8b/maintainability)](https://codeclimate.com/github/RainrainWu/derivation/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/08e384eaba6ad7375e8b/test_coverage)](https://codeclimate.com/github/RainrainWu/derivation/test_coverage)
[![codecov](https://codecov.io/gh/RainrainWu/derivation/branch/master/graph/badge.svg?token=at8Ckp5iLi)](https://codecov.io/gh/RainrainWu/derivation)
[![Github Actions](https://github.com/RainrainWu/derivation/actions/workflows/pull_request.yml/badge.svg)](https://github.com/RainrainWu/derivation/actions/workflows/pull_request.yml)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/derivation.svg)](https://pypi.python.org/pypi/derivation/)

Derivation is a flexible payload generating framework with highly-customizable patterns and rules which raise your efficiency significantly on test case implementation against complicated inputs.

[View Page on Pypi >>](https://pypi.org/project/derivation/)

## Getting Started

### Derivative

Derivative is the primary object which helps you sort out all of possible results with the given inputs.

> The script below can be executed directly
```python
from enum import Enum, auto
from operator import or_

from derivation.constraint import MutuallyExclusiveConstraint, OccurrenceConstraint
from derivation.derivative import Derivative


class DerivativeEvent(Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.upper()


class DerivativeEventExample(DerivativeEvent):

    ESSENTIALS = auto()

    OPTIONAL_1 = auto()
    OPTIONAL_2 = auto()


EVENTS_EXAMPLE = {event: {event.value: None} for event in DerivativeEventExample}

occurrence_constraint = OccurrenceConstraint(
    (DerivativeEventExample.ESSENTIALS,),
    min_times=1,
    max_times=1,
)
mutually_exclusive_constraint = MutuallyExclusiveConstraint(
    (
        DerivativeEventExample.OPTIONAL_1,
        DerivativeEventExample.OPTIONAL_2,
    ),
)
derivative = Derivative(
    EVENTS_EXAMPLE,
    or_,
    (occurrence_constraint, mutually_exclusive_constraint),
)

for order, result in derivative.exhaustive():

    print(f"{order}\n{result}\n")

```

### Constraint

Constraint helps you construct the rules for specific requirements of deriving recipe.

#### Occurrence

Occurrence Constraint make us able to limit the total occurrence times of a specific group of events.

```python
occurrence_constraint = OccurrenceConstraint(
    (DerivativeEventExample.ESSENTIALS,),
    min_times=1,
    max_times=1,
)

# pass
occurrence_constraint.constrain(
    (DerivativeEventExample.ESSENTIALS, DerivativeEventExample.OPTIONAL_1),
)

# error
occurrence_constraint.constrain(
    (DerivativeEventExample.OPTIONAL_1,),
)
```

#### Mutually Exclusive

Occurrence Constraint make us able to avoid conflicts of a specific group of events.

```python
mutually_exclusive_constraint = MutuallyExclusiveConstraint(
    (
        DerivativeEventExample.OPTIONAL_1,
        DerivativeEventExample.OPTIONAL_2,
    ),
)

# pass
mutually_exclusive_constraint.constrain(
    (DerivativeEventExample.ESSENTIALS, DerivativeEventExample.OPTIONAL_1),
)

# error
mutually_exclusive_constraint.constrain(
    (DerivativeEventExample.OPTIONAL_1, DerivativeEventExample.OPTIONAL_2),
)
```

#### Prerequisite

#### Termination