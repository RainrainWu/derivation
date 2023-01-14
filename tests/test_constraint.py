import pytest

from derivation.constraint import PrerequisiteConstraint
from derivation.errors import ConstraintError
from tests.conftest import TestEventAlpha


class TestMutuallyExclusiveConstraint:
    @pytest.mark.parametrize(
        "layers",
        (
            pytest.param(
                (TestEventAlpha.ESSENTIALS,),
            ),
            pytest.param(
                (TestEventAlpha.ESSENTIALS, TestEventAlpha.OPTIONAL_1),
            ),
            pytest.param(
                (TestEventAlpha.ESSENTIALS, TestEventAlpha.OPTIONAL_2),
            ),
            pytest.param(
                (TestEventAlpha.OPTIONAL_2, TestEventAlpha.OPTIONAL_2),
            ),
        ),
    )
    def test_constrain_valid(self, layers, fixture_mutually_exclusive_constraint):

        fixture_mutually_exclusive_constraint.constrain(layers)

    @pytest.mark.parametrize(
        "layers",
        (
            pytest.param(
                (TestEventAlpha.OPTIONAL_2, TestEventAlpha.OPTIONAL_1),
            ),
            pytest.param(
                (TestEventAlpha.OPTIONAL_1, TestEventAlpha.OPTIONAL_2),
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
                (TestEventAlpha.ESSENTIALS,),
            ),
            pytest.param(
                (TestEventAlpha.ESSENTIALS, TestEventAlpha.OPTIONAL_1),
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
                (TestEventAlpha.ESSENTIALS, TestEventAlpha.ESSENTIALS),
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
                (TestEventAlpha.OPTIONAL_1,),
            ),
            pytest.param(
                (TestEventAlpha.ESSENTIALS,),
                (),
            ),
            pytest.param(
                (TestEventAlpha.ESSENTIALS, TestEventAlpha.OPTIONAL_1),
                (TestEventAlpha.OPTIONAL_1, TestEventAlpha.OPTIONAL_2),
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
                (TestEventAlpha.ESSENTIALS,),
            ),
            pytest.param(
                (TestEventAlpha.ESSENTIALS, TestEventAlpha.OPTIONAL_1),
            ),
            pytest.param(
                (TestEventAlpha.ESSENTIALS, TestEventAlpha.OPTIONAL_2),
            ),
            pytest.param(
                (
                    TestEventAlpha.ESSENTIALS,
                    TestEventAlpha.OPTIONAL_1,
                    TestEventAlpha.OPTIONAL_2,
                ),
            ),
            pytest.param(
                (
                    TestEventAlpha.ESSENTIALS,
                    TestEventAlpha.OPTIONAL_2,
                    TestEventAlpha.OPTIONAL_1,
                ),
            ),
            pytest.param(
                (
                    TestEventAlpha.ESSENTIALS,
                    TestEventAlpha.ESSENTIALS,
                    TestEventAlpha.OPTIONAL_1,
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
                (TestEventAlpha.OPTIONAL_1,),
            ),
            pytest.param(
                (TestEventAlpha.OPTIONAL_2,),
            ),
            pytest.param(
                (TestEventAlpha.OPTIONAL_1, TestEventAlpha.ESSENTIALS),
            ),
            pytest.param(
                (
                    TestEventAlpha.ESSENTIALS,
                    TestEventAlpha.OPTIONAL_1,
                    TestEventAlpha.ESSENTIALS,
                ),
            ),
        ),
    )
    def test_constrain_invalid(self, layers, fixture_prerequisite_constraint):

        with pytest.raises(ConstraintError):

            fixture_prerequisite_constraint.constrain(layers)


class TestTerminationConstraint:
    @pytest.mark.parametrize(
        "layers",
        (
            pytest.param(
                (TestEventAlpha.OPTIONAL_1_1,),
            ),
            pytest.param(
                (TestEventAlpha.OPTIONAL_1_1, TestEventAlpha.OPTIONAL_1_2),
            ),
        ),
    )
    def test_constrain_valid(self, layers, fixture_prerequisite_constraint):

        fixture_prerequisite_constraint.constrain(layers)

    @pytest.mark.parametrize(
        "layers",
        (
            pytest.param(
                (),
            ),
            pytest.param(
                (TestEventAlpha.ESSENTIALS,),
            ),
            pytest.param(
                (TestEventAlpha.OPTIONAL_1_1, TestEventAlpha.OPTIONAL_1),
            ),
        ),
    )
    def test_constrain_invalid(self, layers, fixture_termination_constraint):

        with pytest.raises(ConstraintError):

            fixture_termination_constraint.constrain(layers)
