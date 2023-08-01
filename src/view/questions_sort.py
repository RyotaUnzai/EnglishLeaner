
from pathlib import Path

from PySide2 import QtWidgets
from PySide2.QtUiTools import loadUiType

_UI_PATH = Path(__file__).with_name("questions_sort.ui")
_GENERATED_CLASS, _ = loadUiType(_UI_PATH.as_posix())


class Questions_Sort(_GENERATED_CLASS, QtWidgets.QWidget):
    lineEditAnswer: QtWidgets.QLineEdit
    labelJapanese: QtWidgets.QLabel
    labelQuestion: QtWidgets.QLabel
    labelResult: QtWidgets.QLabel
    labelCount: QtWidgets.QLabel
    labelWordsCount: QtWidgets.QLabel
    labelCurrentNumber: QtWidgets.QLabel
    textEditExplanation: QtWidgets.QTextEdit
    pushButtonNext: QtWidgets.QPushButton
    pushButtonPrev: QtWidgets.QPushButton
    pushButtonBack: QtWidgets.QPushButton
    menubar: QtWidgets.QMenuBar
    menuFile: QtWidgets.QMenu
    actionOpen: QtWidgets.QAction
    statusbar: QtWidgets.QStatusBar
    buttonGroup: QtWidgets.QButtonGroup

    def __init__(self, parent=None, *args, **kwargs) -> None:
        super(Questions_Sort, self).__init__(parent, *args, **kwargs)
        self.setupUi(self)
