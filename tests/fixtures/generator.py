from operator import or_

import pytest

from derivation.generator import DerivationGenerator
from tests.common import TEST_LAYERS


@pytest.fixture(scope="function")
def fixture_generator_general(
    fixture_mutually_exclusive_constraint,
    fixture_occurrence_constraint,
    fixture_prerequisite_constraint,
):

    generator = DerivationGenerator(
        TEST_LAYERS,
        or_,
        (
            fixture_mutually_exclusive_constraint,
            fixture_occurrence_constraint,
            fixture_prerequisite_constraint,
        ),
    )

    yield generator
