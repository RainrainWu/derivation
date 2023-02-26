# Derivation

[![Maintainability](https://api.codeclimate.com/v1/badges/08e384eaba6ad7375e8b/maintainability)](https://codeclimate.com/github/RainrainWu/derivation/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/08e384eaba6ad7375e8b/test_coverage)](https://codeclimate.com/github/RainrainWu/derivation/test_coverage)
[![codecov](https://codecov.io/gh/RainrainWu/derivation/branch/master/graph/badge.svg?token=at8Ckp5iLi)](https://codecov.io/gh/RainrainWu/derivation)
[![Github Actions](https://github.com/RainrainWu/derivation/actions/workflows/pull_request.yml/badge.svg)](https://github.com/RainrainWu/derivation/actions/workflows/pull_request.yml)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/derivation.svg)](https://pypi.python.org/pypi/derivation/)

Derivation is a flexible payload generating framework with highly-customizable patterns and rules which raise your efficiency significantly on test case implementation against complicated inputs.

[View Page on Pypi >>](https://pypi.org/project/derivation/)

## Derivative

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

## Constraint

Constraint helps you construct the rules for specific requirements of deriving recipe.

### Occurrence

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

### Mutually Exclusive

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

### Prerequisite

Prerequisite Constraint define the ordering and dependencies of valid event series.

```python
prerequisite_constraint = PrerequisiteConstraint(
    (DerivativeEventExample.ESSENTIALS,),
    (DerivativeEventExample.OPTIONAL_1, DerivativeEventExample.OPTIONAL_2),
)

# pass
prerequisite_constraint.constrain(
    (DerivativeEventExample.ESSENTIALS, DerivativeEventExample.OPTIONAL_1),
)

# error
prerequisite_constraint.constrain(
    (DerivativeEventExample.OPTIONAL_2,),
)
```

### Termination

Termination constraints focus on the specific group of termination events.

```python
termination_constraint = TerminationConstraint(
    (DerivativeEventExample.OPTIONAL_1, DerivativeEventExample.OPTIONAL_2),
)

# pass
termination_constraint.constrain(
    (DerivativeEventExample.ESSENTIALS, DerivativeEventExample.OPTIONAL_1),
)

# error
termination_constraint.constrain(
    (DerivativeEventExample.ESSENTIALS,),
)
```

## Federation

Federation objects allow you construct a more complicated structure with multiple derivation instances, as well as a couple of parameters sets and filtering rules.


> Append script below to the bottom of the previous example for derivation.

```python
from derivation.federation import Federation


class DerivativePatternExample(DerivativeEvent):

    COMPOSITED = auto()


PATTERNS_EXAMPLE = {
    DerivativePatternExample.COMPOSITED: (
        lambda slot_1, slot_2, constant, customized: {
            "slot_1": slot_1,
            "slot_2": slot_2,
            "constant": constant,
            "customized": customized,
        }
    )
}


class DerivativeParamsMapExample(DerivativeEvent):

    DEFAULT = auto()


PARAMS_MAPS_EXAMPLE = {
    DerivativeParamsMapExample.DEFAULT: {"constant": "default"},
}


class DerivativeFilterExample(DerivativeEvent):

    RICH_SLOT_1 = auto()


FILTERS_EXAMPLE = {
    DerivativeFilterExample.RICH_SLOT_1: lambda x: len(x["slot_1"]) > 1,
}

federation = Federation[
    DerivativePatternExample,
    DerivativeParamsMapExample,
    DerivativeFilterExample,
    dict,
](
    {"slot_1": derivative, "slot_2": derivative},
    PATTERNS_EXAMPLE,
    PARAMS_MAPS_EXAMPLE,
    FILTERS_EXAMPLE,
)

for composited_result in federation.exhaustive(
    DerivativePatternExample.COMPOSITED,
    (DerivativeParamsMapExample.DEFAULT,),
    {"customized": "customized"},
    (DerivativeFilterExample.RICH_SLOT_1,),
):

    print(f"{composited_result}\n")
```

### Derivatives & Patterns

Federation object allows you pre-register some patterns which describe how should the derivatives combine with each other.

Pattern are generally a callable function and introduce candidates of the derivatives or apply fixed value as the parameters, we encourage users define readable variable name for better collaboration.

```python
PATTERNS_EXAMPLE = {
    DerivativePatternExample.COMPOSITED: (

        # Callable object as pre-defined pattern.
        lambda slot_1, slot_2, constant, customized: {
            "slot_1": slot_1,
            "slot_2": slot_2,
            "constant": constant,
            "customized": customized,
        }
    )
}
```

### Parameters Maps

For the parameters do not require exhausting via a derivative object, parameters maps can be attached as the fixed values.

```python
PARAMS_MAPS_EXAMPLE = {

    # Apply fixed string object "default" to `constant` parameter inside patterns
    DerivativeParamsMapExample.DEFAULT: {"constant": "default"},
}
```

### Filters

In order to re-use federation object in many similar scenarios, pre-register filters provide a more flexible approach for fetching candidates with specific features.

```python
FILTERS_EXAMPLE = {

    # Only allow results which contain more than one item in slot_1.
    DerivativeFilterExample.RICH_SLOT_1: lambda x: len(x["slot_1"]) > 1,
}
```

### Customized Parameters

Temporary parameters right inside each exhaustive iterator are also supported, which can help you achieve much more flexible design against edge cases.

```python
for composited_result in federation.exhaustive(
    DerivativePatternExample.COMPOSITED,
    (DerivativeParamsMapExample.DEFAULT,),

    # Temporary parameters only take effects within this iterator.
    {"customized": "customized"},
    (DerivativeFilterExample.RICH_SLOT_1,),
):

    print(f"{composited_result}\n")
```

## Contribution

- [RainrainWu](https://github.com/RainrainWu)
