from PyFlow.UI.Canvas.UINodeBase import UINodeBase

from DepthAI.Nodes.Debug.FramePreviewNode import FramePreviewNode
from DepthAI.UI.UIStreamPreviewNode import UIStreamPreviewNode


def createNodeDepthAI(raw_instance):
    if isinstance(raw_instance, FramePreviewNode):
        return UIStreamPreviewNode(raw_instance)
    return UINodeBase(raw_instance)
