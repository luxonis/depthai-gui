import json

from PyFlow.Core import PinBase
from PyFlow.Core.Common import *


class SSenderPacket:
    pass


class NoneEncoder(json.JSONEncoder):
    def default(self, vec3):
        return None


class NoneDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super(NoneDecoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, vec3Dict):
        return SSenderPacket()


class SSenderPin(PinBase):
    """doc string for ImagePin"""

    def __init__(self, name, parent, direction, **kwargs):
        super(SSenderPin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue(SSenderPacket())
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
        return ('SSenderPin',)

    @staticmethod
    def pinDataTypeHint():
        return 'SSenderPin', SSenderPacket()

    @staticmethod
    def color():
        return (100, 150, 100, 127)

    @staticmethod
    def internalDataStructure():
        return SSenderPacket

    @staticmethod
    def processData(data):
        return SSenderPin.internalDataStructure()()
