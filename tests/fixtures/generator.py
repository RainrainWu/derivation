from operator import or_

import pytest

from tests.common import TEST_LAYERS
from variants.generator import VariantsGenerator


@pytest.fixture(scope="function")
def fixture_generator_general(
    fixture_mutually_exclusive_constraint,
    fixture_occurrence_constraint,
    fixture_prerequisite_constraint,
):

    generator = VariantsGenerator(
        TEST_LAYERS,
        or_,
        (
            fixture_mutually_exclusive_constraint,
            fixture_occurrence_constraint,
            fixture_prerequisite_constraint,
        ),
    )

    yield generator
