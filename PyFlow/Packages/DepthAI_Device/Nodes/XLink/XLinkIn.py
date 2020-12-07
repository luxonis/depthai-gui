from common import DeviceNode, get_property_value
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper


class XLinkIn(DeviceNode):
    def __init__(self, name):
        super(XLinkIn, self).__init__(name)
        self.streamName = self.createInputPin('streamName', 'StringPin')
        self.out = self.createOutputPin('out', 'AnyPin')
        self.out.enableOptions(PinOptions.AllowAny)
        self.out.enableOptions(PinOptions.AllowMultipleConnections)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('StringPin')
        helper.addInputStruct(StructureType.Single)
        helper.addOutputDataType('AnyPin')
        helper.addOutputStruct(StructureType.Multi)
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
        xin = pipeline.createXLinkIn()
        xin.setStreamName(get_property_value(self, "streamName"))
        self.connection_map["out"] = xin.out
