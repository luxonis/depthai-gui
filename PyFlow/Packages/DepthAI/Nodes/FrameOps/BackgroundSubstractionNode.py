from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper

from DepthAI.Pins.FramePin import Frame


class BackgroundSubstractionNode(NodeBase):
    def __init__(self, name):
        super(BackgroundSubstractionNode, self).__init__(name)
        self.frame = self.createInputPin('frame', 'FramePin')
        self.out = self.createOutputPin('out', 'FramePin')
        self.out.enableOptions(PinOptions.AllowMultipleConnections)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('FramePin')
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

    def compute(self, *args, **kwargs):
        self.out.setData(Frame())
