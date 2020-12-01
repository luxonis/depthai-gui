from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper

from DepthAI.Pins.H264FramePin import H264Frame


class H264EncodingNode(NodeBase):
    def __init__(self, name):
        super(H264EncodingNode, self).__init__(name)
        self.frame = self.createInputPin('frame', 'FramePin')
        self.encoded = self.createOutputPin('encoded', 'H264FramePin')
        self.encoded.enableOptions(PinOptions.AllowMultipleConnections)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('FramePin')
        helper.addOutputDataType('H264FramePin')
        helper.addOutputStruct(StructureType.Multi)
        return helper

    @staticmethod
    def category():
        return 'Encodings'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return "Description in rst format."

    def compute(self, *args, **kwargs):
        _ = self.frame.getData()
        self.encoded.setData(H264Frame())
