from enum import Enum


class EnumTestLayer(Enum):

    ESSENTIALS = "essentials"

    OPTIONAL_1 = "optional_1"
    OPTIONAL_2 = "optional_2"


TEST_LAYERS = {layer: {str(layer.value): str(layer.value)} for layer in EnumTestLayer}
