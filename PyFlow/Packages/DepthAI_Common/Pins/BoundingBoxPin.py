import json

from PyFlow.Core import PinBase
from PyFlow.Core.Common import *


class BoundingBox:
    pass


class NoneEncoder(json.JSONEncoder):
    def default(self, vec3):
        return None


class NoneDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super(NoneDecoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, vec3Dict):
        return BoundingBox()


class BoundingBoxPin(PinBase):
    """doc string for ImagePin"""

    def __init__(self, name, parent, direction, **kwargs):
        super(BoundingBoxPin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue(BoundingBox())
        self.disableOptions(PinOptions.Storable)

    @staticmethod
    def jsonEncoderClass():
        return NoneEncoder

    @staticmethod
    def jsonDecoderClass():
        return NoneDecoder

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def supportedDataTypes():
        return ('BoundingBoxPin',)

    @staticmethod
    def pinDataTypeHint():
        return 'BoundingBoxPin', BoundingBox()

    @staticmethod
    def color():
        # no. 1 https://coolors.co/3de3f2-2313d4-cdd47f-39cc45-f52ae4-f1f7ad-701068-d2e036-bf2c1f-f5e1f3
        return (61, 227, 242, 255)

    @staticmethod
    def internalDataStructure():
        return BoundingBox

    @staticmethod
    def processData(data):
        return BoundingBoxPin.internalDataStructure()()
