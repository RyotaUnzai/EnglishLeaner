
import sys
from PySide2 import QtWidgets
from view.questions_view import Questions_Window
from model.questions import Questions
from pathlib import Path

RESOURCE_PATH = Path(__file__).parent.with_name("resource").absolute()


class Connect:

    def __init__(self) -> None:
        self.window = Questions_Window()
        self.window.textEditQuestion.setPlainText('Hellow PySide!!')
        self.model = Questions(RESOURCE_PATH / "question_001.json")
        print(self.model.items)
        # print(self.model.items)
        self._setUI()

    def _setUI(self):

        self.window.textEditQuestion.setPlainText(self.model.Question(0))
        # self.window.textEditQuestion = self.model.answer
        # self.window.textEditQuestion = self.model.answer
        # self.window.textEditQuestion = self.model.answer


def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = Connect()
    ex.window.show()
    sys.exit(app.exec_())


main()
