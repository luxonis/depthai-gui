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


class BBoxOverlayNode(HostNode):
    def __init__(self, name):
        super(BBoxOverlayNode, self).__init__(name)
        self.data = self.createInputPin('frame', 'FramePin')
        self.width = self.createInputPin('bbox', 'BoundingBoxPin')
        self.height = self.createInputPin('color_hex', 'StringPin')
        self.frame = self.createOutputPin('result', 'FramePin')
        self.data.enableOptions(PinOptions.AllowMultipleConnections)
        self.frame.enableOptions(PinOptions.AllowMultipleConnections)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('FramePin')
        helper.addInputDataType('BoundingBoxPin')
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

    def get_default(self, name):
        if name == "bbox":
            return []
        return None

    def run(self):        
        if DEBUG:
            print(f"{self.name} waiting...")
        frame, bboxes = self.receive("frame", "bbox")
        if frame is None:        
            if DEBUG:
                print(f"{self.name} skipping - no frame available")
            return
        frame = frame.copy()
        color = hex_to_rgb(get_property_value(self, "color_hex"))
        for raw_bbox in bboxes:
            bbox = frame_norm(frame, *raw_bbox)
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
        self.send("result", frame)        
        if DEBUG:
            print(f"{self.name} updated.")
