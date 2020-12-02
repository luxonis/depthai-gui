from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper

from DepthAI_Common.Pins.FramePin import Frame


class GlobalPropertiesNode(NodeBase):
    def __init__(self, name):
        super(GlobalPropertiesNode, self).__init__(name)
        self.leon_os_freq = self.createInputPin('leon_os_freq', 'IntPin')

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('IntPin')
        helper.addInputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return 'Global'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return "Description in rst format."

    def compute(self, *args, **kwargs):
        pass
