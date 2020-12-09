from pathlib import Path

from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from common import DeviceNode


class FaceDetectionRetail4Node(DeviceNode):
    def __init__(self, name):
        super(FaceDetectionRetail4Node, self).__init__(name)
        self.frame = self.createInputPin('frame', 'FramePin')
        self.out_tensor = self.createOutputPin('out_tensor', 'NeuralTensorPin')
        self.frame.enableOptions(PinOptions.AllowMultipleConnections)
        self.out_tensor.enableOptions(PinOptions.AllowMultipleConnections)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('FramePin')
        helper.addOutputDataType('NeuralTensorPin')
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
        detection_nn.setBlobPath(str(Path(str((Path(__file__).parent / Path('models/face-detection-retail-0004.blob')).resolve().absolute())).resolve().absolute()))
        self.connection_map["out_tensor"] = detection_nn.out
        self.connection_map["frame"] = detection_nn.input
