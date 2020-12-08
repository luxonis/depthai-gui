import numpy as np

from common import HostNode, get_property_value
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from config import DEBUG


class ToBBoxNode(HostNode):
    def __init__(self, name):
        super(ToBBoxNode, self).__init__(name)
        self.data = self.createInputPin('data', 'AnyPin')
        self.threshold = self.createInputPin('threshold', 'FloatPin')
        self.bbox = self.createOutputPin('bbox', 'BoundingBoxPin')
        self.data.enableOptions(PinOptions.AllowAny)
        self.data.enableOptions(PinOptions.AllowMultipleConnections)
        self.bbox.enableOptions(PinOptions.AllowMultipleConnections)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('AnyPin')
        helper.addInputStruct(StructureType.Multi)
        helper.addOutputDataType('FloatPin')
        helper.addOutputStruct(StructureType.Single)
        helper.addOutputDataType('BoundingBoxPin')
        helper.addOutputStruct(StructureType.Multi)
        return helper

    @staticmethod
    def category():
        return 'DataOps'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return "Description in rst format."

    def run(self):
        if DEBUG:
            print(f"{self.name} waiting...")
        nn_data = self.receive("data")
        arr = np.array(nn_data.getFirstLayerFp16())
        arr = arr[:np.where(arr == -1)[0][0]]
        arr = arr.reshape((arr.size // 7, 7))
        arr = [
            obj[3:7]
            for obj in arr
            if obj[2] > get_property_value(self, "threshold")
        ]
        self.send("bbox", arr)
        if DEBUG:
            print(f"{self.name} updated.")
