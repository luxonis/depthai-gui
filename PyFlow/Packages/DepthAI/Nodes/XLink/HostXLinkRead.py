from DepthAI.Nodes.common import HostNode, get_property_value
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper


class HostXLinkRead(HostNode):
    def __init__(self, name):
        super(HostXLinkRead, self).__init__(name)
        self.streamName = self.createInputPin('streamName', 'StringPin')
        self.out = self.createOutputPin('out', 'AnyPin')
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
        print("Initializing XLinkRead with {} queue".format(get_property_value(self, "streamName")))
        self.out = device.getOutputQueue(get_property_value(self, "streamName"), 1, True)

    def run(self):
        print("Starting HostXLinkRead node...")
        while True:
            print("HostXLinkRead waiting...")
            self.send("out", self.out.get())
            print("HostXLinkRead updated.")
