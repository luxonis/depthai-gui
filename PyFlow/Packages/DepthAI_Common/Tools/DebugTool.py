import statistics

from Qt import QtGui
from Qt.QtWidgets import QMessageBox

from DepthAI_Common.Tools import RESOURCES_DIR
from PyFlow.UI.Tool.Tool import ShelfTool
from common import FPS


class DebugTool(ShelfTool):
    """docstring for AlignBottomTool."""

    def __init__(self):
        super(DebugTool, self).__init__()

    @staticmethod
    def toolTip():
        return "Show debug info"

    @staticmethod
    def getIcon():
        return QtGui.QIcon(RESOURCES_DIR + "bug.png")

    @staticmethod
    def name():
        return "Debug"

    def do(self):
        fps_info = "\n".join([
            f"Name: {key} Current: {round(value['current'], 2)} Avg: {round(statistics.mean(value['all']), 2) if len(value['all']) > 0 else 0}"
            for key, value in FPS._data.items()
        ])
        QMessageBox.information(self.pyFlowInstance, "Debug info", f"""
FPS:
{fps_info}
        """)
