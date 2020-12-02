import json

from PyFlow.Core import PinBase
from PyFlow.Core.Common import *


class NeuralTensor:
    pass


class NoneEncoder(json.JSONEncoder):
    def default(self, vec3):
        return None


class NoneDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super(NoneDecoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, vec3Dict):
        return NeuralTensor()


class NeuralTensorPin(PinBase):
    """doc string for ImagePin"""

    def __init__(self, name, parent, direction, **kwargs):
        super(NeuralTensorPin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue(NeuralTensor())
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
        return ('NeuralTensorPin',)

    @staticmethod
    def pinDataTypeHint():
        return 'NeuralTensorPin', NeuralTensor()

    @staticmethod
    def color():
        return (150, 100, 50, 127)

    @staticmethod
    def internalDataStructure():
        return NeuralTensor

    @staticmethod
    def processData(data):
        return NeuralTensorPin.internalDataStructure()()
