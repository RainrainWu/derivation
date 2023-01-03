from unittest import TestCase

import pytest

from tests.common import EnumTestLayer
from variants.errors import ConstraintError, GeneratorError


class TestVariantsGenerator:
    @pytest.mark.parametrize(
        "layers",
        (
            pytest.param(
                (EnumTestLayer.ESSENTIALS,),
            ),
            pytest.param(
                (EnumTestLayer.ESSENTIALS, EnumTestLayer.OPTIONAL_1),
            ),
            pytest.param(
                (EnumTestLayer.ESSENTIALS, EnumTestLayer.OPTIONAL_2),
            ),
        ),
    )
    def test_validate_success(self, layers, fixture_generator_general):

        fixture_generator_general.validate(layers)

    @pytest.mark.parametrize(
        "layers",
        (
            pytest.param(
                (),
            ),
            pytest.param(
                (EnumTestLayer.OPTIONAL_1,),
            ),
            pytest.param(
                (
                    EnumTestLayer.ESSENTIALS,
                    EnumTestLayer.OPTIONAL_1,
                    EnumTestLayer.OPTIONAL_2,
                ),
            ),
        ),
    )
    def test_validate_failed(self, layers, fixture_generator_general):

        with pytest.raises(ConstraintError):
            fixture_generator_general.validate(layers)

    @pytest.mark.parametrize(
        "layers, expected",
        (
            pytest.param(
                (EnumTestLayer.ESSENTIALS,),
                {EnumTestLayer.ESSENTIALS.value: EnumTestLayer.ESSENTIALS.value},
            ),
            pytest.param(
                (EnumTestLayer.ESSENTIALS, EnumTestLayer.OPTIONAL_1),
                {
                    EnumTestLayer.ESSENTIALS.value: EnumTestLayer.ESSENTIALS.value,
                    EnumTestLayer.OPTIONAL_1.value: EnumTestLayer.OPTIONAL_1.value,
                },
            ),
        ),
    )
    def test_accumulate(self, layers, expected, fixture_generator_general):

        TestCase().assertDictEqual(
            fixture_generator_general.accumulate(layers),
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
    def test_accumulate_error(self, layers, fixture_generator_general):

        with pytest.raises(GeneratorError):
            fixture_generator_general.accumulate(layers)
