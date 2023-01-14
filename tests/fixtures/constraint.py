import pytest

from derivation.constraint import (
    MutuallyExclusiveConstraint,
    OccurrenceConstraint,
    PrerequisiteConstraint,
    TerminationConstraint,
)
from tests.conftest import TestEventAlpha


@pytest.fixture(scope="function")
def fixture_mutually_exclusive_constraint():

    constraint = MutuallyExclusiveConstraint(
        (TestEventAlpha.OPTIONAL_1, TestEventAlpha.OPTIONAL_2),
    )

    yield constraint


@pytest.fixture(scope="function")
def fixture_occurrence_constraint():

    constraint = OccurrenceConstraint(
        (TestEventAlpha.ESSENTIALS,),
        min_times=1,
        max_times=1,
    )

    yield constraint


@pytest.fixture(scope="function")
def fixture_prerequisite_constraint():

    constraint = PrerequisiteConstraint(
        (TestEventAlpha.ESSENTIALS,),
        (TestEventAlpha.OPTIONAL_1, TestEventAlpha.OPTIONAL_2),
    )

    yield constraint


@pytest.fixture(scope="function")
def fixture_termination_constraint():

    constraint = TerminationConstraint(
        {
            TestEventAlpha.OPTIONAL_1_1,
            TestEventAlpha.OPTIONAL_1_2,
            TestEventAlpha.OPTIONAL_2_1,
            TestEventAlpha.OPTIONAL_2_2,
        },
    )

    yield constraint
