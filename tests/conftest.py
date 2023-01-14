from enum import Enum, auto

pytest_plugins = [
    "tests.fixtures.constraint",
    "tests.fixtures.derivative",
    "tests.fixtures.federation",
]


class TestEvent(Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.upper()


class TestEventAlpha(TestEvent):

    ESSENTIALS = auto()

    OPTIONAL_1 = auto()
    OPTIONAL_1_1 = auto()
    OPTIONAL_1_2 = auto()

    OPTIONAL_2 = auto()
    OPTIONAL_2_1 = auto()
    OPTIONAL_2_2 = auto()


class TestEventBeta(TestEvent):

    ESSENTIALS = auto()

    OPTIONAL_1 = auto()
    OPTIONAL_2 = auto()


class TestPattern(TestEvent):

    COMBINED = auto()
    NOT_REGISTERED = auto()
    INVALID = auto()


class TestFilter(TestEvent):

    ALPHA_SIZE_GE_3 = auto
    BETA_EMPTY = auto()
