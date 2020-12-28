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


class VideoSourceNode(HostNode):
    def __init__(self, name):
        super(VideoSourceNode, self).__init__(name)
        self.frame = self.createOutputPin('frame', 'FramePin')
        self.frame.enableOptions(PinOptions.AllowMultipleConnections)
        self.file_path = self.createInputPin('file_path', 'StringPin')
        self.file_path.setInputWidgetVariant("FilePathWidget")

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('StringPin')
        helper.addInputStruct(StructureType.Multi)
        helper.addOutputDataType('FramePin')
        helper.addOutputStruct(StructureType.Multi)
        return helper

    @staticmethod
    def category():
        return 'Files'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return "Description in rst format."

    def run(self, device):
        if not get_property_value(self, "file_path"):
            raise RuntimeError(f"No file path specified in {self.name} node!")
        self.cap = cv2.VideoCapture(get_property_value(self, "file_path"))
        while self._running and self.cap.isOpened():
            read_correctly, frame = self.cap.read()
            if read_correctly:
                print("sending video frame...")
                self.send("frame", frame)
                print("video frame sent...")
                time.sleep(0.01)
