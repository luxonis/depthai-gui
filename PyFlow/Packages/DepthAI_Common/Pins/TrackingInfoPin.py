import json

from PyFlow.Core import PinBase
from PyFlow.Core.Common import *


class TrackingInfo:
    pass


class NoneEncoder(json.JSONEncoder):
    def default(self, vec3):
        return None


class NoneDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super(NoneDecoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, vec3Dict):
        return TrackingInfo()


class TrackingInfoPin(PinBase):
    """doc string for ImagePin"""

    def __init__(self, name, parent, direction, **kwargs):
        super(TrackingInfoPin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue(TrackingInfo())
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
        return ('TrackingInfoPin',)

    @staticmethod
    def pinDataTypeHint():
        return 'TrackingInfoPin', TrackingInfo()

    @staticmethod
    def color():
        return (200, 200, 200, 255)

    @staticmethod
    def internalDataStructure():
        return TrackingInfo

    @staticmethod
    def processData(data):
        return TrackingInfoPin.internalDataStructure()()
