from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from common import DeviceNode, get_property_value, get_enum_values


class MonoCameraNode(DeviceNode):
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

    def build_pipeline(self, pipeline):
        import depthai
        cam = pipeline.createMonoCamera()
        cam.setResolution(depthai.MonoCameraProperties.SensorResolution.THE_720_P)
        cam.setResolution(getattr(
            depthai.MonoCameraProperties.SensorResolution,
            get_property_value(self, "resolution", "THE_720_P")
        ))
        self.connection_map["out"] = cam.out
