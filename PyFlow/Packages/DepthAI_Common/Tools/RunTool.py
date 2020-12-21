import traceback

from Qt import QtGui
from Qt.QtWidgets import QMessageBox

from DepthAI_Common.Tools import RESOURCES_DIR
from PyFlow.Core.Common import *
from PyFlow.UI.Tool.Tool import ShelfTool
from common import DeviceNode, HostNode


class RunTool(ShelfTool):
    """docstring for AlignBottomTool."""

    def __init__(self):
        super(RunTool, self).__init__()

    @staticmethod
    def toolTip():
        return "Run pipeline config"

    @staticmethod
    def getIcon():
        return QtGui.QIcon(RESOURCES_DIR + "play.png")

    @staticmethod
    def name():
        return "RunTool"

    def _stop_pipeline(self):
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
            self.device = depthai.Device(pipeline, self.device_info, True)
            self.device.startPipeline()

            self.host_nodes = list(filter(lambda node: isinstance(node, HostNode), rootGraph.getNodesList()))
            for node in self.host_nodes:
                node.run_node(self.device)

        except Exception as e:
            traceback.print_exc()
            QMessageBox.warning(self.pyFlowInstance, "Warning", str(e))
