import cv2
import numpy as np

from common import HostNode, get_property_value
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from config import DEBUG


class ColorMapNode(HostNode):
    def __init__(self, name):
        super(ColorMapNode, self).__init__(name)
        self.data = self.createInputPin('frame', 'FramePin')
        self.color_map = self.createInputPin('color_map', 'StringPin')
        self.color_map.setValueList(list(filter(lambda name: name.startswith('COLORMAP'), dir(cv2))))
        self.frame = self.createOutputPin('result', 'FramePin')
        self.data.enableOptions(PinOptions.AllowMultipleConnections)
        self.frame.enableOptions(PinOptions.AllowMultipleConnections)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('FramePin')
        helper.addInputDataType('StringPin')
        helper.addInputStruct(StructureType.Multi)
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

    def run(self, device):
        color_map = getattr(cv2, get_property_value(self, 'color_map'), cv2.COLORMAP_JET)
        while self._running:
            in_data = self.queue.get()
            if in_data is None:
                continue
            self.send("result", cv2.applyColorMap(in_data['data'], color_map))

