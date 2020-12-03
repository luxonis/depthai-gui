import cv2

from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from Qt import QtGui
from Qt.QtWidgets import QLabel


class UIStreamPreviewNode(UINodeBase):
    def __init__(self, raw_node):
        super(UIStreamPreviewNode, self).__init__(raw_node)
        self.resizable = True
        self.Imagelabel = QLabel("")
        self.pixmap = QtGui.QPixmap(None)
        self.addWidget(self.Imagelabel)
        self.updateSize()

    def Tick(self, *args, **kwargs):
        self.updateSize()
        super(UIStreamPreviewNode, self).Tick(*args, **kwargs)

    def updateSize(self):
        if getattr(self._rawNode, 'display_frame', None) is None:
            return
        frame = self._rawNode.display_frame.copy()
        width = int(self.customLayout.geometry().width())
        height = int(frame.shape[0] * (width / frame.shape[1]))
        display_frame = cv2.cvtColor(cv2.resize(frame, (width, height)), cv2.COLOR_BGR2RGB)
        qImg = QtGui.QImage(display_frame.data, width, height, 3 * width, QtGui.QImage.Format_RGB888)
        self.pixmap = QtGui.QPixmap(qImg)
        self.Imagelabel.setPixmap(self.pixmap)
