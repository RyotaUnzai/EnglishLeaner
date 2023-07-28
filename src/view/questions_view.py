import sys
from PySide2 import QtWidgets


class Example(QtWidgets.QMainWindow):
    def __init__(self, parent=None, *args, **kwargs):
        super(Example, self).__init__(parent, *args, **kwargs)
        self.__initUI()

    def __initUI(self):
        self.setGeometry(500, 300, 400, 270)
        self.setWindowTitle("Menubar & ToolBar & Statusbar")

        openMenu = QtWidgets.QMenu("Open")
        openMenu.addAction("help")

        exitAction = QtWidgets.QAction("Exit", self)
        exitAction.setShortcut("Ctrl+G")
        exitAction.triggered.connect(self.close)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("File")
        fileMenu.addMenu(openMenu)
        fileMenu.addAction(exitAction)

        self.toolbar = self.addToolBar("Exit")
        self.toolbar.addAction(exitAction)

        self.statusBar().showMessage("Ready")


def main():
    app = QtWidgets.QApplication.instance()
    ex = Example()
    ex.show()
    sys.exit()
    app.exec_()


main()
