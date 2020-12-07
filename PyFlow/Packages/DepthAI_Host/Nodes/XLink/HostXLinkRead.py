from common import HostNode, get_property_value
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper


class HostXLinkRead(HostNode):
    def __init__(self, name):
        super(HostXLinkRead, self).__init__(name)
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

    def start(self, device):
        print("Initializing {} with {} queue".format(self.name, get_property_value(self, "streamName")))
        self.out = device.getOutputQueue(get_property_value(self, "streamName"), 1, True)

    def run(self):
        if self.out.has():
            data = self.out.get()
            self.send("out", data)
