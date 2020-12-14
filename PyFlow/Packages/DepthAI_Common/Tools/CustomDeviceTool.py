import json
from pathlib import Path

from DepthAI_Common.Tools import RESOURCES_DIR
from PyFlow import INITIALIZE
from PyFlow.Core.Common import *
from PyFlow.UI.Tool.Tool import ShelfTool
from Qt import QtGui
from Qt.QtWidgets import QMainWindow, QLineEdit, QLabel, QApplication, QCheckBox, QPushButton, QMessageBox


#  https://stackoverflow.com/a/44599922/5494277
def append_to_json(_dict, path):
    with open(path, 'ab+') as f:
        f.seek(0, 2)  # Go to the end of file
        if f.tell() == 0:  # Check if file is empty
            f.write(json.dumps([_dict]).encode())  # If empty, write an array
        else:
            f.seek(-1, 2)
            f.truncate()  # Remove the last character, open the array
            f.write(' , '.encode())  # Write the separator
            f.write(json.dumps(_dict).encode())  # Dump the dictionary
            f.write(']'.encode())


class Second(QMainWindow):
    def __init__(self):
        super(Second, self).__init__()
        self.setWindowTitle("Add new device")

        self.nameLabel = QLabel(self)
        self.nameLabel.move(10, 10)
        self.nameLabel.setText("Device name")
        self.nameEntry = QLineEdit(self)
        self.nameEntry.move(10, 40)
        self.nameEntry.resize(100, 30)

        self.colorLabel = QLabel(self)
        self.colorLabel.move(120, 10)
        self.colorLabel.setText("Color cameras")
        self.colorEntry = QLineEdit(self)
        self.colorEntry.move(140, 40)
        self.colorEntry.resize(70, 30)
        self.colorEntry.setValidator(QtGui.QIntValidator())

        self.monoLabel = QLabel(self)
        self.monoLabel.move(230, 10)
        self.monoLabel.setText("Mono cameras")
        self.monoEntry = QLineEdit(self)
        self.monoEntry.move(250, 40)
        self.monoEntry.resize(70, 30)
        self.monoEntry.setValidator(QtGui.QIntValidator())

        self.depthPresent = QCheckBox("Include depth", self)
        self.depthPresent.move(10, 80)
        self.depthPresent.resize(150, 30)
        self.depthPresent.stateChanged.connect(self.toggle_depth)

        self.leftfovLabel = QLabel(self)
        self.leftfovLabel.move(10, 120)
        self.leftfovLabel.setText("Left FOV deg.")
        self.leftfovEntry = QLineEdit(self)
        self.leftfovEntry.move(180, 120)
        self.leftfovEntry.resize(140, 30)
        self.leftfovEntry.setValidator(QtGui.QDoubleValidator())

        self.rightfovLabel = QLabel(self)
        self.rightfovLabel.move(10, 160)
        self.rightfovLabel.setText("Right FOV deg.")
        self.rightfovEntry = QLineEdit(self)
        self.rightfovEntry.move(180, 160)
        self.rightfovEntry.resize(140, 30)
        self.rightfovEntry.setValidator(QtGui.QDoubleValidator())

        self.rgbfovLabel = QLabel(self)
        self.rgbfovLabel.move(10, 200)
        self.rgbfovLabel.setText("RGB FOV deg.")
        self.rgbfovEntry = QLineEdit(self)
        self.rgbfovEntry.move(180, 200)
        self.rgbfovEntry.resize(140, 30)
        self.rgbfovEntry.setValidator(QtGui.QDoubleValidator())

        self.lrdistanceLabel = QLabel(self)
        self.lrdistanceLabel.move(10, 240)
        self.lrdistanceLabel.resize(200, 30)
        self.lrdistanceLabel.setText("Left - Right distance cm.")
        self.lrdistanceEntry = QLineEdit(self)
        self.lrdistanceEntry.move(180, 240)
        self.lrdistanceEntry.resize(140, 30)
        self.lrdistanceEntry.setValidator(QtGui.QDoubleValidator())

        self.lrgbdistanceLabel = QLabel(self)
        self.lrgbdistanceLabel.move(10, 280)
        self.lrgbdistanceLabel.resize(200, 30)
        self.lrgbdistanceLabel.setText("Left - RGB distance cm.")
        self.lrgbdistanceEntry = QLineEdit(self)
        self.lrgbdistanceEntry.move(180, 280)
        self.lrgbdistanceEntry.resize(140, 30)
        self.lrgbdistanceEntry.setValidator(QtGui.QDoubleValidator())

        self.saveButton = QPushButton("Save", self)
        self.saveButton.resize(100, 30)
        self.saveButton.clicked.connect(self.save)

        self.cancelButton = QPushButton("Cancel", self)
        self.cancelButton.resize(100, 30)
        self.cancelButton.clicked.connect(self.cancel)

        self.toggle_depth(False)

    def toggle_depth(self, checked):
        if checked:
            self.leftfovLabel.setVisible(True)
            self.leftfovEntry.setVisible(True)
            self.rightfovLabel.setVisible(True)
            self.rightfovEntry.setVisible(True)
            self.rgbfovLabel.setVisible(True)
            self.rgbfovEntry.setVisible(True)
            self.lrdistanceLabel.setVisible(True)
            self.lrdistanceEntry.setVisible(True)
            self.lrgbdistanceLabel.setVisible(True)
            self.lrgbdistanceEntry.setVisible(True)
            self.saveButton.move(200, 330)
            self.cancelButton.move(30, 330)
            self.resize(330, 380)
        else:
            self.leftfovLabel.setVisible(False)
            self.leftfovEntry.setVisible(False)
            self.rightfovLabel.setVisible(False)
            self.rightfovEntry.setVisible(False)
            self.rgbfovLabel.setVisible(False)
            self.rgbfovEntry.setVisible(False)
            self.lrdistanceLabel.setVisible(False)
            self.lrdistanceEntry.setVisible(False)
            self.lrgbdistanceLabel.setVisible(False)
            self.lrgbdistanceEntry.setVisible(False)
            self.saveButton.move(200, 120)
            self.cancelButton.move(30, 120)
            self.resize(330, 170)

    def save(self, *args, **kwargs):
        try:
            data = {
                "name": self.nameEntry.text(),
                "color_count": int(self.colorEntry.text()),
                "mono_count": int(self.monoEntry.text()),
            }
            if self.depthPresent.isChecked():
                data.update({
                    "depth": True,
                    "left_fov_deg": float(self.leftfovEntry.text()),
                    "right_fov_deg": float(self.rightfovEntry.text()),
                    "rgb_fov_deg": float(self.rgbfovEntry.text()),
                    "left_to_right_distance_cm": float(self.lrdistanceEntry.text()),
                    "left_to_rgb_distance_cm": float(self.lrgbdistanceEntry.text()),
                })
            append_to_json(data, Path(__file__).parent.parent / Path('custom_devices.json'))
            self.close()
            INITIALIZE()
            self.instance.getRegisteredTools(['NodeBoxTool'])[0].refresh()
        except Exception as e:
            QMessageBox.warning(self, "Warning", str(e))

    def cancel(self):
        self.close()


class CustomDeviceTool(ShelfTool):
    """docstring for AlignBottomTool."""

    def __init__(self):
        super(CustomDeviceTool, self).__init__()
        self.dialog = Second()

    @staticmethod
    def toolTip():
        return "Add custom DepthAI device"

    @staticmethod
    def getIcon():
        return QtGui.QIcon(RESOURCES_DIR + "usb.png")

    @staticmethod
    def name():
        return "CustomDeviceTool"

    def do(self):
        setattr(self.dialog, 'instance', self.pyFlowInstance)
        self.dialog.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Second()
    ex.show()
    sys.exit(app.exec_())
