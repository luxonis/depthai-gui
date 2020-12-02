import json

from PyFlow.Core import PinBase
from PyFlow.Core.Common import *


class H264Frame:
    pass


class NoneEncoder(json.JSONEncoder):
    def default(self, vec3):
        return None


class NoneDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super(NoneDecoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, vec3Dict):
        return H264Frame()


class H264FramePin(PinBase):
    """doc string for ImagePin"""

    def __init__(self, name, parent, direction, **kwargs):
        super(H264FramePin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue(H264Frame())
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
        return ('H264FramePin',)

    @staticmethod
    def pinDataTypeHint():
        return 'H264FramePin', H264Frame()

    @staticmethod
    def color():
        return (200, 100, 50, 127)

    @staticmethod
    def internalDataStructure():
        return H264Frame

    @staticmethod
    def processData(data):
        return H264FramePin.internalDataStructure()()
