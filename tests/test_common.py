import pytest

from derivation.common import adapt_iterable


class TestCommon:
    @pytest.mark.parametrize(
        "_input,expected",
        (
            pytest.param((), ()),
            pytest.param(None, (None,)),
            pytest.param((None,), (None,)),
        ),
    )
    def test_adapt_iterable(self, _input, expected):

        assert adapt_iterable(_input) == expected
