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
from DepthAI_Device.Nodes.Devices.BW1093 import BW1093
from DepthAI_Device.Nodes.Devices.BW1097 import BW1097
from DepthAI_Device.Nodes.Devices.BW1098OBC import BW1098OBC
from DepthAI_Device.Nodes.Devices.BW1098FFC import BW1098FFC
from DepthAI_Device.Nodes.XLink.XLinkIn import XLinkIn
from DepthAI_Device.Nodes.XLink.XLinkOut import XLinkOut
from DepthAI_Device.Nodes.Global.GlobalPropertiesNode import GlobalPropertiesNode
from DepthAI_Device.Nodes.ModelZoo.AgeGenderDetectionNode import AgeGenderDetectionNode
from DepthAI_Device.Nodes.ModelZoo.EmotionsRecognitionNode import EmotionsRecognitionNode
from DepthAI_Device.Nodes.ModelZoo.FaceDetectionAdas1Node import FaceDetectionAdas1Node
from DepthAI_Device.Nodes.ModelZoo.FaceDetectionRetail4Node import FaceDetectionRetail4Node
from DepthAI_Device.Nodes.ModelZoo.FacialLandmarksAdas2Node import FacialLandmarksAdas2Node
from DepthAI_Device.Nodes.ModelZoo.FacialLandmarksRetail9Node import FacialLandmarksRetail9Node
from DepthAI_Device.Nodes.ModelZoo.MobilenetSSDNode import MobilenetSSDNode
from DepthAI_Device.Nodes.ModelZoo.PedestrianDetectionAdas2Node import PedestrianDetectionAdas2Node
from DepthAI_Device.Nodes.ModelZoo.PedestrianDetectionRetail13Node import PedestrianDetectionRetail13Node
from DepthAI_Device.Nodes.ModelZoo.PersonVehicleBikeDetectionNode import PersonVehicleBikeDetectionNode
from DepthAI_Device.Nodes.ModelZoo.VehicleDetectionAdas2Node import VehicleDetectionAdas2Node
from DepthAI_Device.Nodes.ModelZoo.VehicleLicensePlateDetectionNode import VehicleLicensePlateDetectionNode
from DepthAI_Device.Nodes.NeuralNetwork.NeuralNetworkNode import NeuralNetworkNode
from DepthAI_Device.Nodes.Cameras.ColorCameraNode import ColorCameraNode
from DepthAI_Device.Nodes.Cameras.MonoCameraNode import MonoCameraNode
from DepthAI_Device.Nodes.Depth.StereoDepthNode import StereoDepthNode
from DepthAI_Device.Nodes.Encoding.VideoEncoder import VideoEncoder

_FOO_LIBS = {}
_NODES = {}
_PINS = {}
_TOOLS = OrderedDict()
_PREFS_WIDGETS = OrderedDict()
_EXPORTERS = OrderedDict()

NODES_TO_ADD = [
    BW1093, BW1097, BW1098OBC, VehicleLicensePlateDetectionNode, VehicleDetectionAdas2Node, MobilenetSSDNode, BW1098FFC,
    XLinkOut, GlobalPropertiesNode, PedestrianDetectionRetail13Node, XLinkIn, NeuralNetworkNode, AgeGenderDetectionNode,
    EmotionsRecognitionNode, FaceDetectionAdas1Node, FaceDetectionRetail4Node, XLinkBridge, FacialLandmarksAdas2Node,
    FacialLandmarksRetail9Node, PedestrianDetectionAdas2Node, PersonVehicleBikeDetectionNode, MonoCameraNode,
    ColorCameraNode, StereoDepthNode, VideoEncoder
]

for node in NODES_TO_ADD:
    _NODES[node.__name__] = node


class DepthAI_Device(IPackage):
    def __init__(self):
        super(DepthAI_Device, self).__init__()

    @staticmethod
    def GetExporters():
        return _EXPORTERS

    @staticmethod
    def GetFunctionLibraries():
        return _FOO_LIBS

    @staticmethod
    def GetNodeClasses():
        nodes = DepthAI_Device.addDynamicNodes(_NODES.copy())
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
