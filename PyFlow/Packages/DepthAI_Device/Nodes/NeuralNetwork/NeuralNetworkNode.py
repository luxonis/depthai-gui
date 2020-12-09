from pathlib import Path

from common import DeviceNode, get_property_value
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper


class NeuralNetworkNode(DeviceNode):
    def __init__(self, name):
        super(NeuralNetworkNode, self).__init__(name)
        self.input = self.createInputPin('in', 'AnyPin')
        self.blob = self.createInputPin('blob', 'StringPin')
        self.out = self.createOutputPin('out', 'NeuralTensorPin')
        self.blob.setInputWidgetVariant("FilePathWidget")
        self.input.enableOptions(PinOptions.AllowAny)
        self.input.enableOptions(PinOptions.AllowMultipleConnections)
        self.out.enableOptions(PinOptions.AllowMultipleConnections)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('AnyPin')
        helper.addInputDataType('StringPin')
        helper.addOutputDataType('NeuralTensorPin')
        helper.addInputStruct(StructureType.Multi)
        helper.addOutputStruct(StructureType.Multi)
        return helper

    @staticmethod
    def category():
        return 'NeuralNetwork'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return "Description in rst format."

    def build_pipeline(self, pipeline):
        detection_nn = pipeline.createNeuralNetwork()
        path = get_property_value(self, "blob")
        if path is None or len(path) == 0:
            raise RuntimeError(f"Blob file path must be set in the {self.name} node")
        detection_nn.setBlobPath(str(Path(path).resolve().absolute()))
        self.connection_map["out"] = detection_nn.out
        self.connection_map["in"] = detection_nn.input
