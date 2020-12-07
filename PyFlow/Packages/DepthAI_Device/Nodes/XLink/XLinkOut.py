from pathlib import Path

from common import get_property_value, DeviceNode
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper


class XLinkOut(DeviceNode):
    def __init__(self, name):
        super(XLinkOut, self).__init__(name)
        self.streamName = self.createInputPin('streamName', 'StringPin')
        self.input = self.createInputPin('input', 'AnyPin')
        self.input.enableOptions(PinOptions.AllowAny)
        self.input.enableOptions(PinOptions.AllowMultipleConnections)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('StringPin')
        helper.addInputDataType('AnyPin')
        helper.addInputStruct(StructureType.Multi)
        return helper

    @staticmethod
    def category():
        return 'XLink'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return "Description in rst format."

    def build_pipeline(self, pipeline):
        xout = pipeline.createXLinkOut()
        xout.setStreamName(get_property_value(self, "streamName"))
        self.connection_map["input"] = xout.input

