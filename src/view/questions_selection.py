
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
    listView: QtWidgets.QListView

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super(Questions_Selection, self).__init__(parent)
        self.setupUi(self)
        self.listView.setViewMode(QtWidgets.QListView.IconMode)

        self.listView.setResizeMode(QtWidgets.QListView.Adjust)
        self.listView.setFlow(QtWidgets.QListView.LeftToRight)
