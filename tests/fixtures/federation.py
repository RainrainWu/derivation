import pytest

from derivation.federation import Federation
from tests.conftest import TestFilter, TestPattern


@pytest.fixture(scope="function")
def fixture_patterns():

    yield {
        TestPattern.COMBINED: lambda alpha, beta: {"alpha": alpha, "beta": beta},
        TestPattern.INVALID: lambda unknown: unknown,
    }


@pytest.fixture(scope="function")
def fixture_filters():

    yield {
        TestFilter.ALPHA_SIZE_GE_3: lambda x: len(x["alpha"]) > 3,
        TestFilter.BETA_EMPTY: lambda x: not x["beta"],
    }


@pytest.fixture(scope="function")
def fixture_federation(
    fixture_patterns,
    fixture_filters,
    fixture_derivative_general,
    fixture_derivative_beta,
):

    yield Federation[TestPattern, TestFilter, dict](
        {
            "alpha": fixture_derivative_general,
            "beta": fixture_derivative_beta,
        },
        fixture_patterns,
        fixture_filters,
    )
