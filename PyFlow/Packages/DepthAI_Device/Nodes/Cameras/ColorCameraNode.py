from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from common import DeviceNode, get_property_value, get_enum_values


class ColorCameraNode(DeviceNode):
    def __init__(self, name):
        import depthai
        super(ColorCameraNode, self).__init__(name)
        self.preview = self.createOutputPin('preview', 'FramePin')
        self.video = self.createOutputPin('video', 'FramePin')
        self.prev_w = self.createInputPin('prev_width', 'IntPin')
        self.prev_h = self.createInputPin('prev_height', 'IntPin')
        self.resolution = self.createInputPin('resolution', 'StringPin')
        self.interleaved = self.createInputPin('interleaved', 'BoolPin')
        self.resolution.setValueList(get_enum_values(depthai.ColorCameraProperties.SensorResolution))
        self.preview.enableOptions(PinOptions.AllowMultipleConnections)

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
        cam = pipeline.createColorCamera()
        w = get_property_value(self, "prev_width")
        h = get_property_value(self, "prev_height")
        if None not in (w, h) and w > 0 and h > 0:
            cam.setPreviewSize(h, w)
        cam.setResolution(getattr(
            depthai.ColorCameraProperties.SensorResolution,
            get_property_value(self, "resolution", "THE_1080_P")
        ))
        cam.setInterleaved(get_property_value(self, "interleaved"))
        self.connection_map["preview"] = cam.preview
        self.connection_map["video"] = cam.video
