import json
import traceback
from pathlib import Path

import cv2
import numpy as np

from DepthAI.Nodes.common import DepthaiNode, DeviceNode, HostNode
from PyFlow.Core.Common import *
from PyFlow.UI.Tool.Tool import ShelfTool
from Qt import QtGui
from Qt.QtWidgets import QFileDialog, QMessageBox


def get_pin_value(pins, name):
    for pin in pins:
        if pin.name == name:
            return pin.currentData()


def to_nn_result(nn_data):
    return np.array(nn_data.getFirstLayerFp16())


def to_bbox_result(nn_data):
    arr = to_nn_result(nn_data)
    arr = arr[:np.where(arr == -1)[0][0]]
    arr = arr.reshape((arr.size // 7, 7))
    return arr


def frame_norm(frame, *xy_vals):
    height, width = frame.shape[:2]
    result = []
    for i, val in enumerate(xy_vals):
        if i % 2 == 0:
            result.append(max(0, min(width, int(val * width))))
        else:
            result.append(max(0, min(height, int(val * height))))
    return result


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

            self.device = depthai.Device()
            self.device.startPipeline(pipeline)

            host_nodes = list(filter(lambda node: isinstance(node, HostNode), rootGraph.getNodesList()))
            for node in host_nodes:
                node.run_node(self.device)
            # cam_out = self.device.getOutputQueue("cam_out", 1, True)
            # detection_nn = self.device.getOutputQueue("detection_nn")
            # results = []
            # frame = np.zeros((300, 300), np.uint8)
            # while True:
            #     if detection_nn.has():
            #         results = to_bbox_result(detection_nn.get())
            #         print(results)
            #     if cam_out.has():
            #         frame = np.array(cam_out.get().getData()).reshape((3, 300, 300)).transpose(1, 2, 0).astype(np.uint8).copy()
            #     coords = [
            #         frame_norm(frame, *obj[3:7])
            #         for obj in results
            #         if obj[2] > 0.5
            #     ]
            #     for bbox in coords:
            #         cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), 127, 2)
            #     cv2.imshow("Camera_view", frame)
            #     if cv2.waitKey(1) == ord('q'):
            #         break
            print("Done")

        except Exception as e:
            traceback.print_exc()
            QMessageBox.warning(self.pyFlowInstance, "Warning", str(e))

        cv2.destroyAllWindows()

