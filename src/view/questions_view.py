
from pathlib import Path
from PySide2 import QtWidgets
from PySide2.QtUiTools import loadUiType


UI_PATH = Path(__file__).with_name("questions_view.ui")

_GENERATED_CLASS, _ = loadUiType(UI_PATH.as_posix())


class Questions_Window(_GENERATED_CLASS, QtWidgets.QMainWindow):
    lineEditAnswer: QtWidgets.QLineEdit
    textEditQuestion: QtWidgets.QTextEdit
    menubar: QtWidgets.QMenuBar
    menuFile: QtWidgets.QMenu
    actionOpen: QtWidgets.QAction
    statusbar: QtWidgets.QStatusBar

    def __init__(self, *args, **kwargs):
        super(Questions_Window, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.__initUI()

    def __initUI(self):
        self.setWindowTitle("English Questions")

    # @property
    # def lineEditAnswer(self) -> QtWidgets.QLineEdit:
    #     return self.centralWidget().lineEditAnswer

    # @property
    # def textEditQuestion(self) -> QtWidgets.QTextEdit:
    #     return self.centralWidget().textEditQuestion
