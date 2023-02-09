import pytest

from derivation.federation import Federation
from tests.conftest import TestFilter, TestParamsMap, TestPattern


@pytest.fixture(scope="function")
def fixture_patterns():

    yield {
        TestPattern.COMBINED: lambda alpha, beta: {"alpha": alpha, "beta": beta},
        TestPattern.INVALID: lambda unknown: unknown,
    }


@pytest.fixture(scope="function")
def fixture_params_maps():

    yield {
        TestParamsMap.ALPHA_BETA: {"alpha": "alpha", "beta": "beta"},
        TestParamsMap.ALPHA_PATCHED: {"alpha": "alpha patched"},
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
    fixture_params_maps,
    fixture_filters,
    fixture_derivative_alpha,
    fixture_derivative_beta,
):

    yield Federation[TestPattern, TestParamsMap, TestFilter, dict](
        {
            "alpha": fixture_derivative_alpha,
            "beta": fixture_derivative_beta,
        },
        fixture_patterns,
        fixture_params_maps,
        fixture_filters,
    )
