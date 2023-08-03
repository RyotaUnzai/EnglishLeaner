
from pathlib import Path

from PySide2 import QtWidgets
from PySide2.QtUiTools import loadUiType

_UI_PATH = Path(__file__).with_name("questions_selection.ui")
_GENERATED_CLASS, _ = loadUiType(_UI_PATH.as_posix())


class Questions_Selection(_GENERATED_CLASS, QtWidgets.QWidget):
    frameSelection: QtWidgets.QFrame
    labelJapanese: QtWidgets.QLabel
    labelQuestion: QtWidgets.QLabel
    labelWordsCount: QtWidgets.QLabel
    radioButton_0: QtWidgets.QRadioButton
    radioButton_1: QtWidgets.QRadioButton
    radioButton_2: QtWidgets.QRadioButton
    radioButton_3: QtWidgets.QRadioButton
    listView: QtWidgets.QListView
    buttonGroup: QtWidgets.QButtonGroup

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super(Questions_Selection, self).__init__(parent)
        self.setupUi(self)
        self.buttonGroup = QtWidgets.QButtonGroup(self)
        self.buttonGroup.addButton(self.radioButton_0)
        self.buttonGroup.addButton(self.radioButton_1)
        self.buttonGroup.addButton(self.radioButton_2)
        self.buttonGroup.addButton(self.radioButton_3)
        self.listView.setViewMode(QtWidgets.QListView.IconMode)

        self.listView.setResizeMode(QtWidgets.QListView.Adjust)
        self.listView.setFlow(QtWidgets.QListView.LeftToRight)
