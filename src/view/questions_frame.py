
from pathlib import Path

from PySide2 import QtWidgets
from PySide2.QtUiTools import loadUiType
from .questions_selection import Questions_Selection
_UI_PATH = Path(__file__).with_name("questions_frame.ui")
_GENERATED_CLASS, _ = loadUiType(_UI_PATH.as_posix())


class Questions_Frame(_GENERATED_CLASS, QtWidgets.QWidget):
    labelCount: QtWidgets.QLabel
    labelCurrentNumber: QtWidgets.QLabel
    pushButtonNext: QtWidgets.QPushButton
    pushButtonPrev: QtWidgets.QPushButton
    pushButtonBack: QtWidgets.QPushButton
    verticalLayout: QtWidgets.QVBoxLayout
    lineEditAnswer: QtWidgets.QLineEdit
    textEditExplanation: QtWidgets.QTextEdit
    selection: Questions_Selection
    frameExplanation: QtWidgets.QFrame

    def __init__(self, parent=None, *args, **kwargs) -> None:
        super(Questions_Frame, self).__init__(parent, *args, **kwargs)
        self.setupUi(self)
        self.selection = Questions_Selection(self)
        self.verticalLayout.addWidget(self.selection)
        self.frameExplanation.hide()

    def showSort(self):
        super(Questions_Frame, self).show()
        self.selection.frameSelection.hide()

    def showSelection(self):
        super(Questions_Frame, self).show()
        self.selection.frameSelection.show()
