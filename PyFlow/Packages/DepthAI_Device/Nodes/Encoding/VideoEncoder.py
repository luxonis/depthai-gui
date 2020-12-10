from pathlib import Path

from common import DeviceNode, get_property_value, get_enum_values
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper


class VideoEncoder(DeviceNode):
    def __init__(self, name):
        import depthai
        super(VideoEncoder, self).__init__(name)
        self.input = self.createInputPin('input', 'FramePin')
        self.width = self.createInputPin('width', 'IntPin')
        self.height = self.createInputPin('height', 'IntPin')
        self.fps = self.createInputPin('fps', 'IntPin')
        self.profile = self.createInputPin('profile', 'StringPin', defaultValue="H264_MAIN")
        self.bitstream = self.createOutputPin('bitstream', 'EncodedFramePin')
        self.profile.setValueList(get_enum_values(depthai.VideoEncoderProperties.Profile))
        self.input.enableOptions(PinOptions.AllowMultipleConnections)
        self.bitstream.enableOptions(PinOptions.AllowMultipleConnections)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('AnyPin')
        helper.addInputDataType('StringPin')
        helper.addOutputDataType('NeuralTensorPin')
        helper.addInputStruct(StructureType.Multi)
        helper.addOutputStruct(StructureType.Multi)
        return helper

    @staticmethod
    def category():
        return 'Encoding'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return "Description in rst format."

    def build_pipeline(self, pipeline):
        import depthai
        encoder = pipeline.createVideoEncoder()
        if not get_property_value(self, "width"):
            raise RuntimeError(f"Encoder frame width is not specified in {self.name} node!")
        if not get_property_value(self, "height"):
            raise RuntimeError(f"Encoder frame height is not specified in {self.name} node!")
        if not get_property_value(self, "fps"):
            raise RuntimeError(f"Encoder FPS is not specified in {self.name} node!")
        encoder.setDefaultProfilePreset(
            get_property_value(self, "width"),
            get_property_value(self, "height"),
            get_property_value(self, "fps"),
            getattr(depthai.VideoEncoderProperties.Profile, get_property_value(self, "profile", "H264_MAIN"))
        )
        self.connection_map["input"] = encoder.input
        self.connection_map["bitstream"] = encoder.bitstream
