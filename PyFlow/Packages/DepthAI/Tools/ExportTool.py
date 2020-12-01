import json
from pathlib import Path

from PyFlow.Core.Common import *
from PyFlow.UI.Tool.Tool import ShelfTool
from Qt import QtGui
from Qt.QtWidgets import QFileDialog, QMessageBox

from DepthAI.Nodes.Global.GlobalPropertiesNode import GlobalPropertiesNode
from DepthAI.Nodes.common import ExportableNode


def get_pin_value(pins, name):
    for pin in pins:
        if pin.name == name:
            return pin.currentData()


class ExportTool(ShelfTool):
    """docstring for AlignBottomTool."""

    def __init__(self):
        super(ExportTool, self).__init__()

    @staticmethod
    def toolTip():
        return "Export Pipeline Configuration as JSON"

    @staticmethod
    def getIcon():
        return QtGui.QIcon(str((Path(__file__).parent / Path('res/export.png')).resolve().absolute()))

    @staticmethod
    def name():
        return "ExportPipeline"

    def do(self):
        try:
            rootGraph = self.pyFlowInstance.graphManager.get().findRootGraph()
            nodes = []
            connections = []
            global_config = {}
            for node in rootGraph.getNodesList():
                if node.name == GlobalPropertiesNode.__name__:
                    global_config["pipeline_version"] = "test"
                    global_config["Leon OS frequency [kHz]"] = get_pin_value(node.inputs.values(), 'leon_os_freq')
                elif not isinstance(node, ExportableNode):
                    continue
                node, node_connections = node.export()
                nodes.append(node)
                connections += node_connections

            export = json.dumps({
                "globalProperties": global_config,
                "nodes": nodes,
                "connections": connections
            })

            outFilePath, filterString = QFileDialog.getSaveFileName(filter="Pipeline config (*.json)")
            if outFilePath != "":
                with open(outFilePath, 'w') as f:
                    f.write(export)
            print("saved!")
        except Exception as e:
            QMessageBox.warning(self.pyFlowInstance, "Warning", str(e))

