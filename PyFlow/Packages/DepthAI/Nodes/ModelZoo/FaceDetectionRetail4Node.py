from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper

from DepthAI.Pins.BoundingBoxPin import BoundingBox
from DepthAI.Pins.NeuralTensorPin import NeuralTensor


class FaceDetectionRetail4Node(NodeBase):
    def __init__(self, name):
        super(FaceDetectionRetail4Node, self).__init__(name)
        self.frame = self.createInputPin('frame', 'FramePin')
        self.threshold = self.createInputPin('threshold', 'FloatPin')
        self.out_tensor = self.createOutputPin('out_tensor', 'NeuralTensorPin')
        self.bbox = self.createOutputPin('bbox', 'BoundingBoxPin')
        self.depth = self.createOutputPin('depth', 'DepthVectorPin')
        self.frame.enableOptions(PinOptions.AllowMultipleConnections)
        self.bbox.enableOptions(PinOptions.AllowMultipleConnections)
        self.out_tensor.enableOptions(PinOptions.AllowMultipleConnections)
        self.depth.enableOptions(PinOptions.AllowMultipleConnections)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('FramePin')
        helper.addInputDataType('FloatPin')
        helper.addOutputDataType('NeuralTensorPin')
        helper.addOutputDataType('DepthVectorPin')
        helper.addOutputDataType('BoundingBoxPin')
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
        self.bbox.setData(BoundingBox())
