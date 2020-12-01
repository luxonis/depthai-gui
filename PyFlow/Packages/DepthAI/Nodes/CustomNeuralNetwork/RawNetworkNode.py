from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper

from DepthAI.Pins.DetectionLabelPin import DetectionLabel


class RawNetworkNode(NodeBase):
    def __init__(self, name):
        super(RawNetworkNode, self).__init__(name)
        self.frame = self.createInputPin('frame', 'FramePin')
        self.frame.enableOptions(PinOptions.AllowMultipleConnections)
        self.blob_path = self.createInputPin('blob_path', 'StringPin')
        self.config_path = self.createInputPin('config_path', 'StringPin')
        self.label = self.createOutputPin('out_tensor', 'NeuralTensorPin')
        self.label.enableOptions(PinOptions.AllowMultipleConnections)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('FramePin')
        helper.addInputDataType('StringPin')
        helper.addOutputDataType('NeuralTensorPin')
        helper.addInputStruct(StructureType.Multi)
        helper.addOutputStruct(StructureType.Multi)
        return helper

    @staticmethod
    def category():
        return 'Custom Neural Network'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return "Description in rst format."

    def compute(self, *args, **kwargs):
        _ = self.frame.getData()
        self.label.setData(DetectionLabel())
