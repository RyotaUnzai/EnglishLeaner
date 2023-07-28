
from pathlib import Path

from PySide2 import QtWidgets
from PySide2.QtUiTools import loadUiType

UI_PATH = Path(__file__).with_name("questions_view.ui")

_GENERATED_CLASS, _ = loadUiType(UI_PATH.as_posix())


class Questions_Window(_GENERATED_CLASS, QtWidgets.QMainWindow):
    lineEditAnswer: QtWidgets.QLineEdit
    labelQuestion: QtWidgets.QLabel
    labelResult: QtWidgets.QLabel
    textEditExplanation: QtWidgets.QTextEdit
    radioButton_0: QtWidgets.QRadioButton
    radioButton_1: QtWidgets.QRadioButton
    radioButton_2: QtWidgets.QRadioButton
    radioButton_3: QtWidgets.QRadioButton
    pushButtonNext: QtWidgets.QPushButton
    pushButtonPrev: QtWidgets.QPushButton
    menubar: QtWidgets.QMenuBar
    menuFile: QtWidgets.QMenu
    actionOpen: QtWidgets.QAction
    statusbar: QtWidgets.QStatusBar

    def __init__(self, *args, **kwargs) -> None:
        super(Questions_Window, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.__initUI()

    def __initUI(self) -> None:
        self.setWindowTitle("English Questions")

    # @property
    # def lineEditAnswer(self) -> QtWidgets.QLineEdit:
    #     return self.centralWidget().lineEditAnswer

    # @property
    # def textEditQuestion(self) -> QtWidgets.QTextEdit:
    #     return self.centralWidget().textEditQuestion
