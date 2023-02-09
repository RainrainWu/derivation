import pytest

from derivation.errors import FederationError
from tests.conftest import TestFilter, TestParamsMap, TestPattern


class TestFederation:
    def test_federation_exhaustive(self, fixture_federation):

        assert len(tuple(fixture_federation.exhaustive(TestPattern.COMBINED))) == 294
        assert (
            len(
                tuple(
                    fixture_federation.exhaustive(
                        TestPattern.COMBINED,
                        filters_applied=(TestFilter.ALPHA_SIZE_GE_3,),
                    )
                )
            )
            == 182
        )
        assert (
            len(
                tuple(
                    fixture_federation.exhaustive(
                        TestPattern.COMBINED,
                        filters_applied=(TestFilter.BETA_EMPTY,),
                    )
                )
            )
            == 0
        )
        assert (
            len(
                tuple(
                    fixture_federation.exhaustive(
                        TestPattern.COMBINED,
                        params_maps=(TestParamsMap.ALPHA_PATCHED,),
                        filters_applied=(TestFilter.ALPHA_SIZE_GE_3,),
                    )
                )
            )
            == 7
        )
        assert (
            len(
                tuple(
                    fixture_federation.exhaustive(
                        TestPattern.COMBINED,
                        params_maps=(
                            TestParamsMap.ALPHA_BETA,
                            TestParamsMap.ALPHA_PATCHED,
                        ),
                        filters_applied=(TestFilter.ALPHA_SIZE_GE_3,),
                    )
                )
            )
            == 1
        )

    def test_federation_failed_pattern_not_registered(self, fixture_federation):

        with pytest.raises(FederationError):

            tuple(fixture_federation.exhaustive(TestPattern.NOT_REGISTERED))

    def test_federation_failed_invalid_parameters(self, fixture_federation):

        with pytest.raises(FederationError):

            tuple(fixture_federation.exhaustive(TestPattern.INVALID))
