from DepthAI_Common.UI.NodeFactory import createNodeDepthAI
from DepthAI_Common.XLinkBridge import XLinkBridge

PACKAGE_NAME = 'DepthAI'

from collections import OrderedDict
from PyFlow.UI.UIInterfaces import IPackage
import json
from pathlib import Path
from PyFlow.Core.Common import PinOptions
from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper

# Class based nodes
from DepthAI_Host.Nodes.XLink.HostXLinkRead import HostXLinkRead
from DepthAI_Host.Nodes.DataOps.ToBBoxNode import ToBBoxNode
from DepthAI_Host.Nodes.FrameOps.ToFrameNode import ToFrameNode
from DepthAI_Host.Nodes.FrameOps.BBoxOverlayNode import BBoxOverlayNode
from DepthAI_Host.Nodes.Display.FramePreviewNode import FramePreviewNode
from DepthAI_Host.Nodes.Files.FileWriterNode import FileWriterNode

_FOO_LIBS = {}
_NODES = {}
_PINS = {}
_TOOLS = OrderedDict()
_PREFS_WIDGETS = OrderedDict()
_EXPORTERS = OrderedDict()

NODES_TO_ADD = [
    HostXLinkRead, ToFrameNode, FramePreviewNode, BBoxOverlayNode, ToBBoxNode, XLinkBridge, FileWriterNode
]

for node in NODES_TO_ADD:
    _NODES[node.__name__] = node


class DepthAI_Host(IPackage):
    def __init__(self):
        super(DepthAI_Host, self).__init__()

    @staticmethod
    def GetExporters():
        return _EXPORTERS

    @staticmethod
    def GetFunctionLibraries():
        return _FOO_LIBS

    @staticmethod
    def GetNodeClasses():
        nodes = DepthAI_Host.addDynamicNodes(_NODES.copy())
        return nodes

    @staticmethod
    def UINodesFactory():
        return createNodeDepthAI

    @staticmethod
    def GetPinClasses():
        return _PINS

    @staticmethod
    def GetToolClasses():
        return _TOOLS

    @staticmethod
    def addDynamicNodes(nodes):
        path = Path(__file__).parent / Path('custom_devices.json')
        if not path.exists():
            return nodes
        with open(path, 'r') as f:
            data = json.load(f)
        for item in data:
            def node_init(self, name):
                NodeBase.__init__(self, name)
                for i in range(item['color_count']):
                    node_pin = NodeBase.createOutputPin(self, f'color_{i}', 'FramePin')
                    node_pin.enableOptions(PinOptions.AllowMultipleConnections)
                    setattr(self, f'color_{i}', node_pin)
                for i in range(item['mono_count']):
                    node_pin = NodeBase.createOutputPin(self, f'mono_{i}', 'FramePin')
                    node_pin.enableOptions(PinOptions.AllowMultipleConnections)
                    setattr(self, f'mono_{i}', node_pin)

            def node_category():
                return 'Custom Devices'

            def node_compute(self, *args, **kwargs):
                pass

            def node_pin_type_hints():
                helper = NodePinsSuggestionsHelper()
                return helper

            def node_keywords():
                return []

            def node_description(*args, **kwargs):
                return "Description in rst format."

            nodes[item['name']] = type(
                item['name'],
                (NodeBase,),
                {
                    "__init__": node_init,
                    "compute": node_compute
                }
            )
            setattr(nodes[item['name']], 'category', node_category)
            setattr(nodes[item['name']], 'pinTypeHints', node_pin_type_hints)
            setattr(nodes[item['name']], 'keywords', node_keywords)
            setattr(nodes[item['name']], 'description', node_description)
        return nodes
