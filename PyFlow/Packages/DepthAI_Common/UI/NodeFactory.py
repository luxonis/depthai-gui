from PyFlow.UI.Canvas.UINodeBase import UINodeBase

from DepthAI_Common.UI.UIStreamPreviewNode import UIStreamPreviewNode
from common import PreviewNode


def createNodeDepthAI(raw_instance):
    if isinstance(raw_instance, PreviewNode):
        return UIStreamPreviewNode(raw_instance)
    return UINodeBase(raw_instance)
