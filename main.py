from enum import Enum

from variants.constraint import PrerequisiteConstraint


class MyLayer(str, Enum):

    FIRST = "F"
    SECOND = "S"
    THIRD = "T"


c = PrerequisiteConstraint((MyLayer.FIRST, MyLayer.SECOND), (MyLayer.THIRD,))
c.constrain(
    (MyLayer.FIRST, MyLayer.THIRD, MyLayer.FIRST, MyLayer.SECOND, MyLayer.FIRST)
)
