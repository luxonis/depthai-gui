from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper

from DepthAI_Common.Pins.FramePin import Frame


class BW1097(NodeBase):
    def __init__(self, name):
        super(BW1097, self).__init__(name)
        self.color = self.createOutputPin('color', 'FramePin')
        self.mono_l = self.createOutputPin('mono_l', 'FramePin')
        self.mono_r = self.createOutputPin('mono_r', 'FramePin')
        self.color.enableOptions(PinOptions.AllowMultipleConnections)
        self.mono_l.enableOptions(PinOptions.AllowMultipleConnections)
        self.mono_r.enableOptions(PinOptions.AllowMultipleConnections)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addOutputDataType('FramePin')
        helper.addOutputStruct(StructureType.Multi)
        return helper

    @staticmethod
    def category():
        return 'Devices'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return "Description in rst format."

    def compute(self, *args, **kwargs):
        self.color.setData(Frame())
        self.mono_l.setData(Frame())
        self.mono_r.setData(Frame())
