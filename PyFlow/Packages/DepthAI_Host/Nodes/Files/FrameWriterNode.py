from pathlib import Path

import cv2
import numpy as np

from common import HostNode, get_property_value
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from config import DEBUG


class FrameWriterNode(HostNode):
    def __init__(self, name):
        super(FrameWriterNode, self).__init__(name)
        self.data = self.createInputPin('frame', 'FramePin')
        self.dir_path = self.createInputPin('dir_path', 'StringPin')
        self.dir_path.setInputWidgetVariant("FolderPathWidget")
        self.data.enableOptions(PinOptions.AllowAny)
        self.data.enableOptions(PinOptions.AllowMultipleConnections)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('FramePin')
        helper.addInputDataType('StringPin')
        helper.addInputStruct(StructureType.Multi)
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
        if not get_property_value(self, "dir_path"):
            raise RuntimeError(f"No directory path specified in {self.name} node!")
        Path(get_property_value(self, "dir_path")).mkdir(parents=True, exist_ok=True)
        while self._running:
            in_data = self.queue.get()
            if in_data is not None:
                cv2.imwrite(f'{get_property_value(self, "dir_path")}/{int(time.time() * 10000)}.png', in_data['data'])
