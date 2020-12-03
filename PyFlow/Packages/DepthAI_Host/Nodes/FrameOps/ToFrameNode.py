import numpy as np

from common import HostNode, get_property_value
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper


class ToFrameNode(HostNode):
    def __init__(self, name):
        super(ToFrameNode, self).__init__(name)
        self.data = self.createInputPin('data', 'AnyPin')
        self.width = self.createInputPin('width', 'IntPin')
        self.height = self.createInputPin('height', 'IntPin')
        self.frame = self.createOutputPin('frame', 'FramePin')
        self.data.enableOptions(PinOptions.AllowMultipleConnections)
        self.frame.enableOptions(PinOptions.AllowMultipleConnections)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('AnyPin')
        helper.addInputStruct(StructureType.Multi)
        helper.addOutputDataType('FramePin')
        helper.addOutputStruct(StructureType.Multi)
        return helper

    @staticmethod
    def category():
        return 'FrameOps'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return "Description in rst format."

    def run(self):
        print("ToFrame waiting...")
        packet = self.receive("data")
        w = get_property_value(self, "width")
        h = get_property_value(self, "height")
        frame = np.array(packet.getData()).reshape((3, h, w)).transpose(1, 2, 0).astype(np.uint8)
        frame = np.ascontiguousarray(frame)
        self.send("frame", frame)
        print("ToFrame updated.")
