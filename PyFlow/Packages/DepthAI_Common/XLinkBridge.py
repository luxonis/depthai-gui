import string
import random
from common import HostNode, DeviceNode, get_property_value, get_node_by_uid
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper


def get_name():
    return ''.join(random.choice(string.ascii_letters) for i in range(12))


class XLinkBridge(HostNode, DeviceNode):
    def __init__(self, name):
        super(XLinkBridge, self).__init__(name)
        self.out = self.createInputPin('in', 'AnyPin')
        self.out = self.createOutputPin('out', 'AnyPin')
        self.out.enableOptions(PinOptions.AllowMultipleConnections)
        self.name = get_name()

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
        if self.to_host():
            print("Initializing XLinkRead with {} queue".format(self.name))
            self.out = device.getOutputQueue(self.name, 1, True)
        else:
            self.input = device.getInputQueue(self.name)

    def run(self):
        if self.to_host():
            print("HostXLinkRead waiting...")
            data = self.out.get()
            self.send("out", data)
            print("HostXLinkRead updated.")
        else:
            print("HostXLinkRead waiting...")
            data = self.receive("in")
            self.input.send(data)
            print("HostXLinkRead updated.")
