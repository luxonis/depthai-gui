from pathlib import Path

import cv2
import numpy as np

from common import HostNode, get_property_value
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from config import DEBUG


def hex_to_rgb(hex_string):
    r_hex = hex_string[1:3]
    g_hex = hex_string[3:5]
    b_hex = hex_string[5:7]
    return int(r_hex, 16), int(g_hex, 16), int(b_hex, 16)


def frame_norm(frame, *xy_vals):
    height, width = frame.shape[:2]
    result = []
    for i, val in enumerate(xy_vals):
        if i % 2 == 0:
            result.append(max(0, min(width, int(val * width))))
        else:
            result.append(max(0, min(height, int(val * height))))
    return result


class DataFeederNode(HostNode):
    def __init__(self, name):
        super(DataFeederNode, self).__init__(name)
        self.data = self.createInputPin('data', 'StringPin')
        self.data.enableOptions(PinOptions.AllowAny)
        self.out = self.createOutputPin('out', 'AnyPin')
        self.out.enableOptions(PinOptions.AllowAny)
        self.out.enableOptions(PinOptions.AllowMultipleConnections)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addOutputDataType('AnyPin')
        helper.addOutputStruct(StructureType.Multi)
        return helper

    @staticmethod
    def category():
        return 'Debug'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return "Description in rst format."

    def run(self, device):
        while self._running:
            data = get_property_value(self, "data")
            self.send("out", eval(data))
