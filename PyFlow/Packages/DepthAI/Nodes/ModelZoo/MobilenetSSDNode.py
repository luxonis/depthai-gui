from pathlib import Path

from DepthAI.Nodes.common import DeviceNode
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper


class MobilenetSSDNode(DeviceNode):
    def __init__(self, name):
        super(MobilenetSSDNode, self).__init__(name)
        self.frame = self.createInputPin('frame', 'FramePin')
        self.threshold = self.createInputPin('threshold', 'FloatPin')
        self.out_tensor = self.createOutputPin('out_tensor', 'NeuralTensorPin')
        # self.bbox = self.createOutputPin('bbox', 'BoundingBoxPin')
        # self.depth = self.createOutputPin('depth', 'DepthVectorPin')
        # self.label = self.createOutputPin('label', 'DetectionLabelPin')
        self.frame.enableOptions(PinOptions.AllowMultipleConnections)
        self.out_tensor.enableOptions(PinOptions.AllowMultipleConnections)
        # self.bbox.enableOptions(PinOptions.AllowMultipleConnections)
        # self.depth.enableOptions(PinOptions.AllowMultipleConnections)
        # self.label.enableOptions(PinOptions.AllowMultipleConnections)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('FramePin')
        helper.addInputDataType('FloatPin')
        helper.addOutputDataType('NeuralTensorPin')
        # helper.addOutputDataType('DepthVectorPin')
        # helper.addOutputDataType('BoundingBoxPin')
        # helper.addOutputDataType('DetectionLabelPin')
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

    def build_pipeline(self, pipeline):
        detection_nn = pipeline.createNeuralNetwork()
        detection_nn.setBlobPath(str(Path(str((Path(__file__).parent / Path('models/mobilenet-ssd.blob')).resolve().absolute())).resolve().absolute()))
        self.connection_map["out_tensor"] = detection_nn.out
        self.connection_map["frame"] = detection_nn.input
