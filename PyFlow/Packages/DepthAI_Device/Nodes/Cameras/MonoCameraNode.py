from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from common import get_property_value, get_enum_values, CameraNode


class MonoCameraNode(CameraNode):
    def __init__(self, name):
        import depthai
        super(MonoCameraNode, self).__init__(name)
        self.out = self.createOutputPin('out', 'FramePin')
        self.out.enableOptions(PinOptions.AllowMultipleConnections)
        self.resolution = self.createInputPin('resolution', 'StringPin')
        self.resolution.setValueList(get_enum_values(depthai.MonoCameraProperties.SensorResolution))

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addOutputDataType('FramePin')
        helper.addOutputStruct(StructureType.Multi)
        return helper

    @staticmethod
    def category():
        return 'Cameras'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return "Description in rst format."

    def getId(self):
        nodes = self.getWrapper().canvasRef().graphManager.findRootGraph().getNodesList()
        cams = list(sorted(map(lambda node: node.name, filter(lambda node: isinstance(node, MonoCameraNode), nodes))))
        cam_idx = cams.index(self.name)
        if cam_idx == 0:
            return 1
        else:
            return 2

    def build_pipeline(self, pipeline):
        import depthai
        cam = pipeline.createMonoCamera()
        cam.setResolution(getattr(
            depthai.MonoCameraProperties.SensorResolution,
            get_property_value(self, "resolution", "THE_720_P")
        ))
        cam.setCamId(self.getId())
        self.connection_map["out"] = cam.out
