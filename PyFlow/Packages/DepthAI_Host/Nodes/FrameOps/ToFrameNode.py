import numpy as np

from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from common import HostNode, get_property_value


class ToFrameNode(HostNode):
    def __init__(self, name):
        super(ToFrameNode, self).__init__(name)
        self.data = self.createInputPin('data', 'AnyPin')
        self.data.enableOptions(PinOptions.AllowAny)
        self.out = self.createOutputPin('out', 'FramePin')
        self.out.enableOptions(PinOptions.AllowMultipleConnections)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('AnyPin')
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

    def run(self, device):
        while self._running:
            data = self.queue.get()
            if data is None:
                continue
            arr = data['data'].getData()
            w = data['data'].getWidth()
            h = data['data'].getHeight()
            channels = arr.size / (w * h)
            if not channels.is_integer():
                raise RuntimeError(f"Width/Height is incorrect for the data received (size: {arr.size}, calc_n_channels: {channels})")
            if channels == 1:
                frame = arr.reshape((h, w)).astype(np.uint8)
            else:
                frame = arr.reshape((int(channels), h, w)).transpose(1, 2, 0).astype(np.uint8)
            frame = np.ascontiguousarray(frame)
            self.send("out", frame)
