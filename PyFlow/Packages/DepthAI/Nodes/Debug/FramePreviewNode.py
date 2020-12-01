import cv2

from DepthAI.Nodes.common import HostNode, get_property_value
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper


class FramePreviewNode(HostNode):
    def __init__(self, name):
        super(FramePreviewNode, self).__init__(name)
        self.frame = self.createInputPin('frame', 'FramePin')
        self.frame.enableOptions(PinOptions.AllowMultipleConnections)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('FramePin')
        helper.addInputStruct(StructureType.Multi)
        helper.addInputDataType('StringPin')
        helper.addInputStruct(StructureType.Single)
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

    def run(self, *args, **kwargs):
        print("Starting preview node...")
        while True:
            print("Preview waiting...")
            self.display_frame = self.receive("data")
            print("Preview updated.")
