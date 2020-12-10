from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from common import DeviceNode, get_property_value, get_enum_values


class StereoDepthNode(DeviceNode):
    def __init__(self, name):
        import depthai
        super(StereoDepthNode, self).__init__(name)
        self.syncedLeft = self.createOutputPin('syncedLeft', 'FramePin')
        self.syncedRight = self.createOutputPin('syncedRight', 'FramePin')
        self.depth = self.createOutputPin('depth', 'FramePin')
        self.disparity = self.createOutputPin('disparity', 'FramePin')
        self.rectifiedLeft = self.createOutputPin('rectifiedLeft', 'FramePin')
        self.rectifiedRight = self.createOutputPin('rectifiedRight', 'FramePin')
        self.left = self.createInputPin('left', 'FramePin')
        self.right = self.createInputPin('right', 'FramePin')
        self.median = self.createInputPin('median', 'StringPin')
        self.raw_depth = self.createInputPin('raw_depth', 'BoolPin')
        self.rectified = self.createInputPin('rectified', 'BoolPin')
        self.lr_check = self.createInputPin('lr_check', 'BoolPin')
        self.ext_disparity = self.createInputPin('ext_disparity', 'BoolPin')
        self.subpixel = self.createInputPin('subpixel', 'BoolPin')
        self.median.setValueList(get_enum_values(depthai.StereoDepthProperties.MedianFilter))
        self.syncedLeft.enableOptions(PinOptions.AllowMultipleConnections)
        self.syncedRight.enableOptions(PinOptions.AllowMultipleConnections)
        self.depth.enableOptions(PinOptions.AllowMultipleConnections)
        self.disparity.enableOptions(PinOptions.AllowMultipleConnections)
        self.rectifiedLeft.enableOptions(PinOptions.AllowMultipleConnections)
        self.rectifiedRight.enableOptions(PinOptions.AllowMultipleConnections)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('BoolPin')
        helper.addOutputDataType('FramePin')
        helper.addInputStruct(StructureType.Multi)
        helper.addOutputStruct(StructureType.Multi)
        return helper

    @staticmethod
    def category():
        return 'Depth'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return "Description in rst format."

    def build_pipeline(self, pipeline):
        import depthai
        depth = pipeline.createStereoDepth()
        depth.setConfidenceThreshold(200)
        depth.setOutputDepth(get_property_value(self, "raw_depth"))
        depth.setOutputRectified(get_property_value(self, "rectified"))
        depth.setRectifyEdgeFillColor(0)  # Black, to better see the cutout
        depth.setMedianFilter(getattr(
            depthai.StereoDepthProperties.MedianFilter,
            get_property_value(self, "median", "MEDIAN_OFF")
        ))
        depth.setLeftRightCheck(get_property_value(self, "lr_check"))
        depth.setExtendedDisparity(get_property_value(self, "ext_disparity"))
        depth.setSubpixel(get_property_value(self, "subpixel"))
        self.connection_map["syncedLeft"] = depth.syncedLeft
        self.connection_map["syncedRight"] = depth.syncedRight
        self.connection_map["depth"] = depth.depth
        self.connection_map["disparity"] = depth.disparity
        self.connection_map["rectifiedLeft"] = depth.rectifiedLeft
        self.connection_map["rectifiedRight"] = depth.rectifiedRight
