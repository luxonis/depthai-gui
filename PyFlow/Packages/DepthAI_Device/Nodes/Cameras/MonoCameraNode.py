from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from common import DeviceNode, get_property_value


class ColorCameraNode(DeviceNode):
    def __init__(self, name):
        super(ColorCameraNode, self).__init__(name)
        self.out = self.createOutputPin('out', 'FramePin')
        self.prev_w = self.createInputPin('prev_width', 'IntPin')
        self.prev_h = self.createInputPin('prev_height', 'IntPin')
        self.out.enableOptions(PinOptions.AllowMultipleConnections)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('IntPin')
        helper.addOutputDataType('FramePin')
        helper.addInputStruct(StructureType.Multi)
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
        w = get_property_value(self, "prev_width")
        h = get_property_value(self, "prev_height")
        if None not in (w, h) and w > 0 and h > 0:
            cam.setPreviewSize(h, w)
        cam.setResolution(depthai.MonoCameraProperties.SensorResolution.THE_720_P)
        self.connection_map["out"] = cam.preview
