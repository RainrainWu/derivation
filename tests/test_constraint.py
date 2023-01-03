import pytest

from tests.common import EnumTestLayer
from variants.constraint import (
    PrerequisiteConstraint,
)
from variants.errors import ConstraintError


class TestMutuallyExclusiveConstraint:
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
            pytest.param(
                (EnumTestLayer.OPTIONAL_2, EnumTestLayer.OPTIONAL_2),
            ),
        ),
    )
    def test_constrain_valid(self, layers, fixture_mutually_exclusive_constraint):

        fixture_mutually_exclusive_constraint.constrain(layers)

    @pytest.mark.parametrize(
        "layers",
        (
            pytest.param(
                (EnumTestLayer.OPTIONAL_2, EnumTestLayer.OPTIONAL_1),
            ),
            pytest.param(
                (EnumTestLayer.OPTIONAL_1, EnumTestLayer.OPTIONAL_2),
            ),
        ),
    )
    def test_constrain_invalid(self, layers, fixture_mutually_exclusive_constraint):

        with pytest.raises(ConstraintError):

            fixture_mutually_exclusive_constraint.constrain(layers)


class TestOccurrenceConstraint:
    @pytest.mark.parametrize(
        "layers",
        (
            pytest.param(
                (EnumTestLayer.ESSENTIALS,),
            ),
            pytest.param(
                (EnumTestLayer.ESSENTIALS, EnumTestLayer.OPTIONAL_1),
            ),
        ),
    )
    def test_constrain_valid(self, layers, fixture_occurrence_constraint):

        fixture_occurrence_constraint.constrain(layers)

    @pytest.mark.parametrize(
        "layers",
        (
            pytest.param(
                (),
            ),
            pytest.param(
                (EnumTestLayer.ESSENTIALS, EnumTestLayer.ESSENTIALS),
            ),
        ),
    )
    def test_constrain_invalid(self, layers, fixture_occurrence_constraint):

        with pytest.raises(ConstraintError):

            fixture_occurrence_constraint.constrain(layers)


class TestPrerequisiteConstraint:
    @pytest.mark.parametrize(
        "layers_prerequisite, layers_subsequent",
        (
            pytest.param(
                (),
                (EnumTestLayer.OPTIONAL_1,),
            ),
            pytest.param(
                (EnumTestLayer.ESSENTIALS,),
                (),
            ),
            pytest.param(
                (EnumTestLayer.ESSENTIALS, EnumTestLayer.OPTIONAL_1),
                (EnumTestLayer.OPTIONAL_1, EnumTestLayer.OPTIONAL_2),
            ),
        ),
    )
    def test_construct_error(self, layers_prerequisite, layers_subsequent):

        with pytest.raises(ConstraintError):
            PrerequisiteConstraint(
                layers_prerequisite,
                layers_subsequent,
            )

    @pytest.mark.parametrize(
        "layers",
        (
            pytest.param(
                (),
            ),
            pytest.param(
                (EnumTestLayer.ESSENTIALS,),
            ),
            pytest.param(
                (EnumTestLayer.ESSENTIALS, EnumTestLayer.OPTIONAL_1),
            ),
            pytest.param(
                (EnumTestLayer.ESSENTIALS, EnumTestLayer.OPTIONAL_2),
            ),
            pytest.param(
                (
                    EnumTestLayer.ESSENTIALS,
                    EnumTestLayer.OPTIONAL_1,
                    EnumTestLayer.OPTIONAL_2,
                ),
            ),
            pytest.param(
                (
                    EnumTestLayer.ESSENTIALS,
                    EnumTestLayer.OPTIONAL_2,
                    EnumTestLayer.OPTIONAL_1,
                ),
            ),
            pytest.param(
                (
                    EnumTestLayer.ESSENTIALS,
                    EnumTestLayer.ESSENTIALS,
                    EnumTestLayer.OPTIONAL_1,
                ),
            ),
        ),
    )
    def test_constrain_valid(self, layers, fixture_prerequisite_constraint):

        fixture_prerequisite_constraint.constrain(layers)

    @pytest.mark.parametrize(
        "layers",
        (
            pytest.param(
                (EnumTestLayer.OPTIONAL_1,),
            ),
            pytest.param(
                (EnumTestLayer.OPTIONAL_2,),
            ),
            pytest.param(
                (EnumTestLayer.OPTIONAL_1, EnumTestLayer.ESSENTIALS),
            ),
            pytest.param(
                (
                    EnumTestLayer.ESSENTIALS,
                    EnumTestLayer.OPTIONAL_1,
                    EnumTestLayer.ESSENTIALS,
                ),
            ),
        ),
    )
    def test_constrain_invalid(self, layers, fixture_prerequisite_constraint):

        with pytest.raises(ConstraintError):

            fixture_prerequisite_constraint.constrain(layers)
