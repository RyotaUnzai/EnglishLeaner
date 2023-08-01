
from pathlib import Path

from PySide2 import QtWidgets
from PySide2.QtUiTools import loadUiType
from .questions_frame import Questions_Frame
from .questions_menu import Questions_Menu

_UI_PATH = Path(__file__).with_name("questions_view.ui")
_GENERATED_CLASS, _ = loadUiType(_UI_PATH.as_posix())


class Questions_Window(_GENERATED_CLASS, QtWidgets.QMainWindow):
    frame: Questions_Frame
    menu: Questions_Menu
    verticalLayout: QtWidgets.QVBoxLayout
    sender_widget: QtWidgets.QPushButton
    currentMode = "menu"

    def __init__(self, *args, **kwargs) -> None:
        super(Questions_Window, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.frame = Questions_Frame(self)

        self.frame.hide()
        self.menu = Questions_Menu(self)
        self.verticalLayout.addWidget(self.frame)
        self.verticalLayout.addWidget(self.menu)
        self.__initUI()

    def __initUI(self) -> None:
        self.setWindowTitle("English Questions")
        self.menu.pushButtonSelection.clicked.connect(lambda: self.showUI(mode="selection"))
        self.menu.pushButtonSort.clicked.connect(lambda: self.showUI(mode="sort"))
        self.frame.pushButtonBack.clicked.connect(lambda: self.showUI(mode="menu"))

    def showUI(self, mode: str) -> None:
        geometry = self.geometry()
        self.sender_widget = self.sender()
        self.currentMode = mode
        if self.currentMode == "selection":
            self.showSelection()
        elif self.currentMode == "sort":
            self.showSort()
        elif self.currentMode == "menu":
            self.showMenu()
        self.setGeometry(geometry)

    def showSort(self) -> None:
        self.menu.hide()
        self.frame.showSort()

    def showSelection(self) -> None:
        self.menu.hide()
        self.frame.showSelection()

    def showMenu(self) -> None:
        self.frame.hide()
        self.menu.show()
