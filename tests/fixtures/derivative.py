from operator import __add__, or_

import pytest

from derivation.derivative import Derivative
from tests.conftest import TestEventAlpha, TestEventBeta


@pytest.fixture(scope="session")
def fixture_events_alpha():

    yield {event: {event.value: None} for event in TestEventAlpha}


@pytest.fixture(scope="session")
def fixture_events_beta():

    yield {event: [event.value] for event in TestEventBeta}


@pytest.fixture(scope="function")
def fixture_derivative_alpha(
    fixture_events_alpha,
    fixture_mutually_exclusive_constraint,
    fixture_occurrence_constraint,
    fixture_prerequisite_constraint,
    fixture_termination_constraint,
):

    derivative = Derivative(
        fixture_events_alpha,
        or_,
        (
            fixture_mutually_exclusive_constraint,
            fixture_occurrence_constraint,
            fixture_prerequisite_constraint,
            fixture_termination_constraint,
        ),
    )

    yield derivative


@pytest.fixture(scope="function")
def fixture_derivative_beta(fixture_events_beta):

    yield Derivative(fixture_events_beta, __add__)
