PACKAGE_NAME = 'DepthAI'

from collections import OrderedDict
from PyFlow.UI.UIInterfaces import IPackage
import json
from pathlib import Path
from PyFlow.Core.Common import PinOptions
from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper

# Class based nodes
from DepthAI.Nodes.Test.DemoNode import DemoNode
from DepthAI.Nodes.Test.MyProducer import MyProducer
from DepthAI.Nodes.Devices.BW1093 import BW1093
from DepthAI.Nodes.Devices.BW1097 import BW1097
from DepthAI.Nodes.Devices.BW1098OBC import BW1098OBC
from DepthAI.Nodes.Devices.BW1098FFC import BW1098FFC
from DepthAI.Nodes.Debug.FramePreviewNode import FramePreviewNode
from DepthAI.Nodes.CustomNeuralNetwork.ClassificationNetworkNode import ClassificationNetworkNode
from DepthAI.Nodes.CustomNeuralNetwork.DetectorNetworkNode import DetectorNetworkNode
from DepthAI.Nodes.CustomNeuralNetwork.OCRNetworkNode import OCRNetworkNode
from DepthAI.Nodes.CustomNeuralNetwork.RawNetworkNode import RawNetworkNode
from DepthAI.Nodes.XLink.XLinkIn import XLinkIn
from DepthAI.Nodes.XLink.XLinkOut import XLinkOut
from DepthAI.Nodes.Global.GlobalPropertiesNode import GlobalPropertiesNode
from DepthAI.Nodes.Encodings.H264EncodingNode import H264EncodingNode
from DepthAI.Nodes.Encodings.H265EncodingNode import H265EncodingNode
from DepthAI.Nodes.FrameOps.ROICropNode import ROICropNode
from DepthAI.Nodes.FrameOps.DepthLocationNode import DepthLocationNode
from DepthAI.Nodes.FrameOps.ObjectTrackerNode import ObjectTrackerNode
from DepthAI.Nodes.FrameOps.DigitalZoomNode import DigitalZoomNode
from DepthAI.Nodes.FrameOps.BackgroundSubstractionNode import BackgroundSubstractionNode
from DepthAI.Nodes.ModelZoo.AgeGenderDetectionNode import AgeGenderDetectionNode
from DepthAI.Nodes.ModelZoo.EmotionsRecognitionNode import EmotionsRecognitionNode
from DepthAI.Nodes.ModelZoo.FaceDetectionAdas1Node import FaceDetectionAdas1Node
from DepthAI.Nodes.ModelZoo.FaceDetectionRetail4Node import FaceDetectionRetail4Node
from DepthAI.Nodes.ModelZoo.FacialLandmarksAdas2Node import FacialLandmarksAdas2Node
from DepthAI.Nodes.ModelZoo.FacialLandmarksRetail9Node import FacialLandmarksRetail9Node
from DepthAI.Nodes.ModelZoo.MobilenetSSDNode import MobilenetSSDNode
from DepthAI.Nodes.ModelZoo.OCRNode import OCRNode
from DepthAI.Nodes.ModelZoo.PedestrianDetectionAdas2Node import PedestrianDetectionAdas2Node
from DepthAI.Nodes.ModelZoo.PedestrianDetectionRetail13Node import PedestrianDetectionRetail13Node
from DepthAI.Nodes.ModelZoo.PersonVehicleBikeDetectionNode import PersonVehicleBikeDetectionNode
from DepthAI.Nodes.ModelZoo.VehicleDetectionAdas2Node import VehicleDetectionAdas2Node
from DepthAI.Nodes.ModelZoo.VehicleLicensePlateDetectionNode import VehicleLicensePlateDetectionNode
from DepthAI.Nodes.FrameOps.ToFrameNode import ToFrameNode
from DepthAI.Nodes.XLink.HostXLinkRead import HostXLinkRead

# Pins
from DepthAI.Pins.FramePin import FramePin
from DepthAI.Pins.BoundingBoxPin import BoundingBoxPin
from DepthAI.Pins.DetectionLabelPin import DetectionLabelPin
from DepthAI.Pins.NeuralTensorPin import NeuralTensorPin
from DepthAI.Pins.DepthVectorPin import DepthVectorPin
from DepthAI.Pins.MSenderPin import MSenderPin
from DepthAI.Pins.SSenderPin import SSenderPin
from DepthAI.Pins.H264FramePin import H264FramePin
from DepthAI.Pins.H265FramePin import H265FramePin
from DepthAI.Pins.TrackingInfoPin import TrackingInfoPin

# Tools
from DepthAI.Tools.ExportTool import ExportTool
from DepthAI.Tools.CustomDeviceTool import CustomDeviceTool
from DepthAI.Tools.RunTool import RunTool

# Factories
from DepthAI.UI.NodeFactory import createNodeDepthAI

_FOO_LIBS = {}
_NODES = {}
_PINS = {}
_TOOLS = OrderedDict()
_PREFS_WIDGETS = OrderedDict()
_EXPORTERS = OrderedDict()

NODES_TO_ADD = [
    DemoNode, MyProducer, BW1093, BW1097, BW1098OBC, VehicleLicensePlateDetectionNode, VehicleDetectionAdas2Node,
    XLinkOut, GlobalPropertiesNode, ClassificationNetworkNode, H264EncodingNode, H265EncodingNode, ROICropNode, XLinkIn,
    DetectorNetworkNode, DepthLocationNode, ObjectTrackerNode, DigitalZoomNode, BackgroundSubstractionNode, BW1098FFC,
    AgeGenderDetectionNode, EmotionsRecognitionNode, FaceDetectionAdas1Node, FaceDetectionRetail4Node, OCRNetworkNode,
    FacialLandmarksAdas2Node, FacialLandmarksRetail9Node, MobilenetSSDNode, OCRNode, PedestrianDetectionAdas2Node,
    PedestrianDetectionRetail13Node, PersonVehicleBikeDetectionNode, RawNetworkNode, FramePreviewNode, ToFrameNode,
    HostXLinkRead
]

for node in NODES_TO_ADD:
    _NODES[node.__name__] = node

PINS_TO_ADD = [
    FramePin, NeuralTensorPin, BoundingBoxPin, DetectionLabelPin, DepthVectorPin, MSenderPin, SSenderPin, H264FramePin,
    H265FramePin, TrackingInfoPin
]

for pin in PINS_TO_ADD:
    _PINS[pin.__name__] = pin

TOOLS_TO_ADD = [ExportTool, CustomDeviceTool, RunTool]

for tool in TOOLS_TO_ADD:
    _TOOLS[tool.__name__] = tool


class DepthAI(IPackage):
    def __init__(self):
        super(DepthAI, self).__init__()

    @staticmethod
    def GetExporters():
        return _EXPORTERS

    @staticmethod
    def GetFunctionLibraries():
        return _FOO_LIBS

    @staticmethod
    def GetNodeClasses():
        nodes = DepthAI.addDynamicNodes(_NODES.copy())
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
