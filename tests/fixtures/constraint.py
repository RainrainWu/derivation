import pytest

from tests.common import EnumTestLayer
from variants.constraint import (
    MutuallyExclusiveConstraint,
    OccurrenceConstraint,
    PrerequisiteConstraint,
)


@pytest.fixture(scope="function")
def fixture_mutually_exclusive_constraint():

    constraint = MutuallyExclusiveConstraint(
        (EnumTestLayer.OPTIONAL_1, EnumTestLayer.OPTIONAL_2),
    )

    yield constraint


@pytest.fixture(scope="function")
def fixture_occurrence_constraint():

    constraint = OccurrenceConstraint(
        (EnumTestLayer.ESSENTIALS,),
        min_times=1,
        max_times=1,
    )

    yield constraint


@pytest.fixture(scope="function")
def fixture_prerequisite_constraint():

    constraint = PrerequisiteConstraint(
        (EnumTestLayer.ESSENTIALS,),
        (EnumTestLayer.OPTIONAL_1, EnumTestLayer.OPTIONAL_2),
    )

    yield constraint
