
from pathlib import Path

from PySide2 import QtWidgets
from PySide2.QtUiTools import loadUiType

_UI_PATH = Path(__file__).with_name("questions_menu.ui")
_GENERATED_CLASS, _ = loadUiType(_UI_PATH.as_posix())


class Questions_Menu(_GENERATED_CLASS, QtWidgets.QWidget):
    pushButtonSelection: QtWidgets.QPushButton
    pushButtonSort: QtWidgets.QPushButton
    pushButtonWrite: QtWidgets.QPushButton

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super(Questions_Menu, self).__init__(parent)
        self.setupUi(self)
