from unittest import TestCase

import pytest

from derivation.errors import ConstraintError, DerivativeError
from tests.conftest import TestEventAlpha


class TestDerivative:
    @pytest.mark.parametrize(
        "layers",
        (
            pytest.param(
                (TestEventAlpha.ESSENTIALS, TestEventAlpha.OPTIONAL_1_1),
            ),
            pytest.param(
                (
                    TestEventAlpha.ESSENTIALS,
                    TestEventAlpha.OPTIONAL_1,
                    TestEventAlpha.OPTIONAL_1_2,
                ),
            ),
        ),
    )
    def test_validate_success(self, layers, fixture_derivative_alpha):

        fixture_derivative_alpha.validate(layers)

    @pytest.mark.parametrize(
        "layers",
        (
            pytest.param(
                (),
            ),
            pytest.param(
                (TestEventAlpha.OPTIONAL_1,),
            ),
            pytest.param(
                (
                    TestEventAlpha.ESSENTIALS,
                    TestEventAlpha.OPTIONAL_1,
                    TestEventAlpha.OPTIONAL_2,
                ),
            ),
        ),
    )
    def test_validate_failed(self, layers, fixture_derivative_alpha):

        with pytest.raises(ConstraintError):

            fixture_derivative_alpha.validate(layers)

    @pytest.mark.parametrize(
        "layers, expected",
        (
            pytest.param(
                (TestEventAlpha.ESSENTIALS, TestEventAlpha.OPTIONAL_1_1),
                {
                    TestEventAlpha.ESSENTIALS.value: None,
                    TestEventAlpha.OPTIONAL_1_1.value: None,
                },
            ),
            pytest.param(
                (
                    TestEventAlpha.ESSENTIALS,
                    TestEventAlpha.OPTIONAL_1,
                    TestEventAlpha.OPTIONAL_1_1,
                ),
                {
                    TestEventAlpha.ESSENTIALS.value: None,
                    TestEventAlpha.OPTIONAL_1.value: None,
                    TestEventAlpha.OPTIONAL_1_1.value: None,
                },
            ),
        ),
    )
    def test_derive(self, layers, expected, fixture_derivative_alpha):

        TestCase().assertDictEqual(
            fixture_derivative_alpha.derive(layers),
            expected,
        )

    @pytest.mark.parametrize(
        "layers",
        (
            pytest.param(
                (),
            ),
        ),
    )
    def test_derive_error(self, layers, fixture_derivative_alpha):

        with pytest.raises(DerivativeError):

            fixture_derivative_alpha.derive(layers)

    def test_exhaustive(self, fixture_derivative_alpha):

        assert len(tuple(fixture_derivative_alpha.exhaustive())) == 42
