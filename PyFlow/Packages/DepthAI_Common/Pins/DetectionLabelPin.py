import json

from PyFlow.Core import PinBase
from PyFlow.Core.Common import *


class DetectionLabel:
    pass


class NoneEncoder(json.JSONEncoder):
    def default(self, vec3):
        return None


class NoneDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super(NoneDecoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, vec3Dict):
        return DetectionLabel()


class DetectionLabelPin(PinBase):
    """doc string for ImagePin"""

    def __init__(self, name, parent, direction, **kwargs):
        super(DetectionLabelPin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue(DetectionLabel())
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
        return ('DetectionLabelPin',)

    @staticmethod
    def pinDataTypeHint():
        return 'DetectionLabelPin', DetectionLabel()

    @staticmethod
    def color():
        return (100, 200, 50, 127)

    @staticmethod
    def internalDataStructure():
        return DetectionLabel

    @staticmethod
    def processData(data):
        return DetectionLabelPin.internalDataStructure()()
