from PyFlow.UI.Utils.stylesheet import Colors

from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from common import DeviceNode, HostNode


class XLinkToHost(HostNode, DeviceNode):
    def __init__(self, name):
        super(XLinkToHost, self).__init__(name)
        self.headerColor = Colors.NodeNameRectOrange.getRgb()
        self.input = self.createInputPin('in', 'AnyPin')
        self.input.enableOptions(PinOptions.AllowAny)
        self.out = self.createOutputPin('out', 'AnyPin')
        self.out.enableOptions(PinOptions.AllowAny)
        self.out.enableOptions(PinOptions.AllowMultipleConnections)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
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
        xout = pipeline.createXLinkOut()
        xout.setStreamName(self.name)
        self.connection_map["in"] = xout.input

    def run(self, device):
        q_in = device.getOutputQueue(self.name)
        while self._running:
            self.send("out", q_in.get())
