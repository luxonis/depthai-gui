import numpy as np

from common import HostNode, get_property_value
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from config import DEBUG


class ToFrameNode(HostNode):
    def __init__(self, name):
        super(ToFrameNode, self).__init__(name)
        self.data = self.createInputPin('data', 'AnyPin')
        self.width = self.createInputPin('width', 'IntPin')
        self.height = self.createInputPin('height', 'IntPin')
        self.frame = self.createOutputPin('frame', 'FramePin')
        self.data.enableOptions(PinOptions.AllowAny)
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
        if DEBUG:
            print(f"{self.name} waiting...")
        packet = self.receive("data")
        w = get_property_value(self, "width")
        h = get_property_value(self, "height")
        if 0 in (w, h):
            raise RuntimeError(f"Width/Height is not set on the {self.name} node")
        arr = np.array(packet.getData())
        channels = arr.size / (w * h)
        if not channels.is_integer():
            raise RuntimeError(f"Width/Height is incorrect for the data received (size: {arr.size}, calc_n_channels: {channels})")
        if channels == 1:
            frame = arr.reshape((h, w)).astype(np.uint8)
        else:
            frame = arr.reshape((int(channels), h, w)).transpose(1, 2, 0).astype(np.uint8)
        frame = np.ascontiguousarray(frame)
        self.send("frame", frame)
        if DEBUG:
            print(f"{self.name} updated.")
