import json
import traceback
from pathlib import Path

import cv2
import numpy as np

from common import DepthaiNode, DeviceNode, HostNode
from PyFlow.Core.Common import *
from PyFlow.UI.Tool.Tool import ShelfTool
from Qt import QtGui
from Qt.QtWidgets import QFileDialog, QMessageBox


class RunTool(ShelfTool):
    """docstring for AlignBottomTool."""

    def __init__(self):
        super(RunTool, self).__init__()

    @staticmethod
    def toolTip():
        return "Run pipeline config"

    @staticmethod
    def getIcon():
        return QtGui.QIcon(str((Path(__file__).parent / Path('res/play.png')).resolve().absolute()))

    @staticmethod
    def name():
        return "RunPipeline"

    def stop_pipeline(self):
        for node in self.host_nodes:
            node.stop_node()
        del self.device

    def do(self):
        try:
            import depthai
            pipeline = depthai.Pipeline()
            rootGraph = self.pyFlowInstance.graphManager.get().findRootGraph()
            device_nodes = list(filter(lambda node: isinstance(node, DeviceNode), rootGraph.getNodesList()))
            for node in device_nodes:
                node.build_pipeline(pipeline)
            for node in device_nodes:
                node.build_connections()

            self.found, self.device_info = depthai.XLinkConnection.getFirstDevice(depthai.XLinkDeviceState.X_LINK_UNBOOTED)
            if not self.found:
                raise RuntimeError("Device not found")
            self.device = depthai.Device(self.device_info, True)
            self.device.startPipeline(pipeline)

            self.host_nodes = list(filter(lambda node: isinstance(node, HostNode), rootGraph.getNodesList()))
            for node in self.host_nodes:
                node.run_node(self.device)

        except Exception as e:
            traceback.print_exc()
            QMessageBox.warning(self.pyFlowInstance, "Warning", str(e))
