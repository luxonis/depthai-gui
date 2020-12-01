import json

from PyFlow.Core import PinBase
from PyFlow.Core.Common import *


class MSenderPacket:
    pass


class NoneEncoder(json.JSONEncoder):
    def default(self, vec3):
        return None


class NoneDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super(NoneDecoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, vec3Dict):
        return MSenderPacket()


class MSenderPin(PinBase):
    """doc string for ImagePin"""

    def __init__(self, name, parent, direction, **kwargs):
        super(MSenderPin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue(MSenderPacket())
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
        return ('MSenderPin',)

    @staticmethod
    def pinDataTypeHint():
        return 'MSenderPin', MSenderPacket()

    @staticmethod
    def color():
        return (150, 100, 50, 127)

    @staticmethod
    def internalDataStructure():
        return MSenderPacket

    @staticmethod
    def processData(data):
        return MSenderPin.internalDataStructure()()
