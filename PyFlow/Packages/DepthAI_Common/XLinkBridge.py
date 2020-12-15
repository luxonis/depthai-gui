import queue
import string
import random
import threading

from common import HostNode, DeviceNode, get_property_value, get_node_by_uid, DepthaiNode, get_pin_by_index
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.UI.Utils.stylesheet import Colors
from config import DEBUG


class XLinkBridge(HostNode, DeviceNode):
    def __init__(self, name):
        super(XLinkBridge, self).__init__(name)
        self.headerColor = Colors.NodeNameRectOrange.getRgb()
        self.input = self.createInputPin('in', 'AnyPin')
        self.out = self.createOutputPin('out', 'AnyPin')
        self.input.enableOptions(PinOptions.AllowAny)
        self.out.enableOptions(PinOptions.AllowAny)
        self.out.enableOptions(PinOptions.AllowMultipleConnections)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('AnyPin')
        helper.addInputStruct(StructureType.Single)
        helper.addOutputDataType('AnyPin')
        helper.addOutputStruct(StructureType.Multi)
        return helper

    @staticmethod
    def category():
        return 'XLink'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return "Description in rst format."

    def to_host(self):
        nodes = self.getWrapper().canvasRef().graphManager.findRootGraph().getNodesList()
        out = next(iter(self.outputs.values()))
        for link in out.linkedTo:
            connected_node = get_node_by_uid(nodes, link['rhsNodeUid'])
            if isinstance(connected_node, HostNode):
                return True
            elif isinstance(connected_node, DeviceNode):
                return False
            else:
                raise RuntimeError("Connected node is neither Device nor Host node")

    def build_pipeline(self, pipeline):
        if self.to_host():
            xout = pipeline.createXLinkOut()
            xout.setStreamName(self.name)
            self.connection_map["in"] = xout.input
        else:
            xin = pipeline.createXLinkIn()
            xin.setStreamName(self.name)
            self.connection_map["out"] = xin.out

    def start(self, device):
        self._running = True
        if self.to_host():
            print("Initializing {} with {} queue".format(self.name, self.name))
            self.out = device.getOutputQueue(self.name, 1, True)
        else:
            self.input = device.getInputQueue(self.name)

    def run_node(self, device):
        if self.to_host():
            self.thread = threading.Thread(target=self.run_to_host, args=(device, ), daemon=True)
            self.thread.start()
        else:
            self.queue = queue.Queue()
            self.thread = threading.Thread(target=self.run_to_device, args=(self.queue, ), daemon=True)
            self.thread.start()

    def stop_node(self, wait=True):
        self._running = False
        if wait:
            self.thread.join()

    def run_to_host(self, device):
        self.setup_connections()
        self.start(device)
        while self._running:
            data = self.out.tryGet()
            if data is not None:
                if DEBUG:
                    print(f"{self.name} got new data...")
                self.send("out", data)
                if DEBUG:
                    print(f"{self.name} updated.")

    def run_to_device(self, queue):
        self.queue = queue
        self.input_buffer = {}
        while self._running:
            self.get_queue_data()
            data = self.receive("in")
            if data is not None:
                if DEBUG:
                    print(f"{self.name} got new data...")
                self.input.send(data)
                if DEBUG:
                    print(f"{self.name} updated.")
