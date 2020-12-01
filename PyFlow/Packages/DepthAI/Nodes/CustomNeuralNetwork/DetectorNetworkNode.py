from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper

from DepthAI.Pins.DetectionLabelPin import DetectionLabel


class DetectorNetworkNode(NodeBase):
    def __init__(self, name):
        super(DetectorNetworkNode, self).__init__(name)
        self.frame = self.createInputPin('frame', 'FramePin')
        self.frame.enableOptions(PinOptions.AllowMultipleConnections)
        self.blob_path = self.createInputPin('blob_path', 'StringPin')
        self.config_path = self.createInputPin('config_path', 'StringPin')
        self.threshold = self.createInputPin('threshold', 'FloatPin')
        self.label = self.createOutputPin('label', 'DetectionLabelPin')
        self.bbox = self.createOutputPin('bbox', 'BoundingBoxPin')
        self.depth = self.createOutputPin('depth', 'DepthVectorPin')
        self.label.enableOptions(PinOptions.AllowMultipleConnections)
        self.bbox.enableOptions(PinOptions.AllowMultipleConnections)
        self.depth.enableOptions(PinOptions.AllowMultipleConnections)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('FramePin')
        helper.addInputDataType('FloatPin')
        helper.addInputDataType('StringPin')
        helper.addInputDataType('NeuralNetworkPin')
        helper.addOutputDataType('DetectionLabelPin')
        helper.addOutputDataType('BoundingBoxPin')
        helper.addOutputDataType('DepthVectorPin')
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
        _ = self.threshold.getData()
        self.label.setData(DetectionLabel())
