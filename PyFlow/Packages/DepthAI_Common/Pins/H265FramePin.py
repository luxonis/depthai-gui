import json

from PyFlow.Core import PinBase
from PyFlow.Core.Common import *


class H265Frame:
    pass


class NoneEncoder(json.JSONEncoder):
    def default(self, vec3):
        return None


class NoneDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super(NoneDecoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, vec3Dict):
        return H265Frame()


class H265FramePin(PinBase):
    """doc string for ImagePin"""

    def __init__(self, name, parent, direction, **kwargs):
        super(H265FramePin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue(H265Frame())
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
        return ('H265FramePin',)

    @staticmethod
    def pinDataTypeHint():
        return 'H265FramePin', H265Frame()

    @staticmethod
    def color():
        return (100, 150, 50, 127)

    @staticmethod
    def internalDataStructure():
        return H265Frame

    @staticmethod
    def processData(data):
        return H265FramePin.internalDataStructure()()
