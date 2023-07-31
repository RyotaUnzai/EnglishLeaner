
from pathlib import Path

from PySide2 import QtWidgets
from PySide2.QtUiTools import loadUiType

WINDOW_UI_PATH = Path(__file__).with_name("questions_view.ui")

MENU_UI_PATH = Path(__file__).with_name("questions_menu.ui")
SELECTION_UI_PATH = Path(__file__).with_name("questions_selection.ui")
SORT_UI_PATH = Path(__file__).with_name("questions_sort.ui")
_GENERATED_WINDOW_CLASS, _ = loadUiType(WINDOW_UI_PATH.as_posix())
_GENERATED_MENU_CLASS, _ = loadUiType(MENU_UI_PATH.as_posix())
_GENERATED_SELECTION_CLASS, _ = loadUiType(SELECTION_UI_PATH.as_posix())
_GENERATED_SORT_CLASS, _ = loadUiType(SORT_UI_PATH.as_posix())


class Questions_Selection(_GENERATED_SELECTION_CLASS, QtWidgets.QWidget):
    lineEditAnswer: QtWidgets.QLineEdit
    labelJapanese: QtWidgets.QLabel
    labelQuestion: QtWidgets.QLabel
    labelResult: QtWidgets.QLabel
    labelCount: QtWidgets.QLabel
    labelCurrentNumber: QtWidgets.QLabel
    textEditExplanation: QtWidgets.QTextEdit
    radioButton_0: QtWidgets.QRadioButton
    radioButton_1: QtWidgets.QRadioButton
    radioButton_2: QtWidgets.QRadioButton
    radioButton_3: QtWidgets.QRadioButton
    pushButtonNext: QtWidgets.QPushButton
    pushButtonPrev: QtWidgets.QPushButton
    pushButtonBack: QtWidgets.QPushButton
    menubar: QtWidgets.QMenuBar
    menuFile: QtWidgets.QMenu
    actionOpen: QtWidgets.QAction
    statusbar: QtWidgets.QStatusBar
    buttonGroup: QtWidgets.QButtonGroup

    def __init__(self, parent=None, *args, **kwargs) -> None:
        super(Questions_Selection, self).__init__(parent, *args, **kwargs)
        self.setupUi(self)
        self.buttonGroup = QtWidgets.QButtonGroup()
        for num in range(4):
            exec(f"self.buttonGroup.addButton(self.radioButton_{num})")


class Questions_Sort(_GENERATED_SORT_CLASS, QtWidgets.QWidget):
    lineEditAnswer: QtWidgets.QLineEdit
    labelJapanese: QtWidgets.QLabel
    labelQuestion: QtWidgets.QLabel
    labelResult: QtWidgets.QLabel
    labelCount: QtWidgets.QLabel
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


class Questions_Menu(_GENERATED_MENU_CLASS, QtWidgets.QWidget):
    pushButtonSelection: QtWidgets.QPushButton
    pushButtonSort: QtWidgets.QPushButton

    def __init__(self, parent=None, *args, **kwargs) -> None:
        super(Questions_Menu, self).__init__(parent, *args, **kwargs)
        self.setupUi(self)


class Questions_Window(_GENERATED_WINDOW_CLASS, QtWidgets.QMainWindow):
    menu: Questions_Menu
    sort: Questions_Sort
    selection: Questions_Selection
    verticalLayout: QtWidgets.QVBoxLayout

    def __init__(self, *args, **kwargs) -> None:
        super(Questions_Window, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.menu = Questions_Menu(self)
        self.sort = Questions_Sort(self)
        self.selection = Questions_Selection(self)
        self.__initUI()

    def __initUI(self) -> None:
        self.setWindowTitle("English Questions")
        self.showSectionMenu()
        self.verticalLayout.addWidget(self.sort)
        self.verticalLayout.addWidget(self.selection)
        self.verticalLayout.addWidget(self.menu)

        self.menu.pushButtonSelection.clicked.connect(self.showSectionSelection)
        self.menu.pushButtonSort.clicked.connect(self.showSectionSort)
        self.sort.pushButtonBack.clicked.connect(self.showSectionMenu)
        self.selection.pushButtonBack.clicked.connect(self.showSectionMenu)

    def showSectionSort(self) -> None:
        geometry = self.geometry()
        self.selection.hide()
        self.menu.hide()
        self.sort.show()
        self.setGeometry(geometry)

    def showSectionSelection(self) -> None:
        geometry = self.geometry()
        self.sort.hide()
        self.menu.hide()
        self.selection.show()
        self.setGeometry(geometry)

    def showSectionMenu(self) -> None:
        geometry = self.geometry()
        self.selection.hide()
        self.sort.hide()
        self.menu.show()
        self.setGeometry(geometry)
