from PyFlow.UI.Utils.stylesheet import Colors

from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from common import DeviceNode, HostNode


class XLinkToDevice(HostNode, DeviceNode):
    def __init__(self, name):
        super(XLinkToDevice, self).__init__(name)
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
        xin = pipeline.createXLinkIn()
        xin.setStreamName(self.name)
        self.connection_map["out"] = xin.out

    def run(self, device):
        q_out = device.getInputQueue(self.name)
        while self._running:
            in_data = self.queue.get()
            if in_data is not None:
                q_out.send(in_data['data'])
