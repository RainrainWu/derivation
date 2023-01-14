import pytest

from derivation.errors import FederationError
from tests.conftest import TestFilter, TestPattern


class TestFederation:
    def test_federation_exhaustive(self, fixture_federation):

        assert len(tuple(fixture_federation.exhaustive(TestPattern.COMBINED))) == 294
        assert (
            len(
                tuple(
                    fixture_federation.exhaustive(
                        TestPattern.COMBINED, (TestFilter.ALPHA_SIZE_GE_3,)
                    )
                )
            )
            == 182
        )
        assert (
            len(
                tuple(
                    fixture_federation.exhaustive(
                        TestPattern.COMBINED, (TestFilter.BETA_EMPTY,)
                    )
                )
            )
            == 0
        )

    def test_federation_failed_pattern_not_registered(self, fixture_federation):

        with pytest.raises(FederationError):

            tuple(fixture_federation.exhaustive(TestPattern.NOT_REGISTERED))

    def test_federation_failed_invalid_parameters(self, fixture_federation):

        with pytest.raises(FederationError):

            tuple(fixture_federation.exhaustive(TestPattern.INVALID))
