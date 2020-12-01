from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper

from DepthAI.Pins.NeuralTensorPin import NeuralTensor


class OCRNode(NodeBase):
    def __init__(self, name):
        super(OCRNode, self).__init__(name)
        self.frame = self.createInputPin('frame', 'FramePin')
        self.out_tensor = self.createOutputPin('text', 'StringPin')
        self.frame.enableOptions(PinOptions.AllowMultipleConnections)
        self.out_tensor.enableOptions(PinOptions.AllowMultipleConnections)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('FramePin')
        helper.addOutputDataType('StringPin')
        helper.addInputStruct(StructureType.Multi)
        helper.addOutputStruct(StructureType.Multi)
        return helper

    @staticmethod
    def category():
        return 'Model Zoo'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return "Description in rst format."

    def compute(self, *args, **kwargs):
        _ = self.frame.getData()
        self.out_tensor.setData(NeuralTensor())
