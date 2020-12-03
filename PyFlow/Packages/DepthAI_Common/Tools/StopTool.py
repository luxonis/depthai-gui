import traceback
from pathlib import Path

from Qt import QtGui
from Qt.QtWidgets import QMessageBox

from DepthAI_Common import RunTool
from PyFlow.Core.Common import *
from PyFlow.UI.Tool.Tool import ShelfTool
from common import DeviceNode, HostNode


class StopTool(ShelfTool):
    """docstring for AlignBottomTool."""

    def __init__(self):
        super(StopTool, self).__init__()

    @staticmethod
    def toolTip():
        return "Stop running pipeline"

    @staticmethod
    def getIcon():
        return QtGui.QIcon(str((Path(__file__).parent / Path('res/stop.png')).resolve().absolute()))

    @staticmethod
    def name():
        return "StopPipeline"

    def do(self):
        try:
            run_tool = next(filter(lambda tool: tool.name() == RunTool.name(), self.pyFlowInstance._tools), None)
            if run_tool is not None:
                print("STOPPING!")
                run_tool.stop_pipeline()

        except Exception as e:
            traceback.print_exc()
            QMessageBox.warning(self.pyFlowInstance, "Warning", str(e))
