import random
import sys
from pathlib import Path

from PySide2 import QtWidgets

from model.questions import Questions
from view.questions_view import Questions_Window

QSS_PATH = Path(__file__).parent / "view" / "questions_view.qss"
RESOURCE_PATH = Path(__file__).parent.with_name("resource").absolute()


class Connect:
    __numbers: list = []
    __current: int = 0

    def __init__(self) -> None:
        self.window = Questions_Window()
        self.model = Questions(RESOURCE_PATH / "question_001.json")
        # print(self.model.items)
        self.setQuestion(0)
        self.setNumbers()
        self._setUI()

    def _setUI(self) -> None:
        self.loadQSS()
        
        self.window.lineEditAnswer.returnPressed.connect(self.result)
        self.window.pushButtonNext.clicked.connect(self.nextQuestion)
        self.window.pushButtonPrev.clicked.connect(self.prevQuestion)

    def loadQSS(self) -> None:
        with open(QSS_PATH.absolute().as_posix(), encoding="utf-8") as f:
            self.window.setStyleSheet(f.read())

    def setNumbers(self) -> None:
        self.__numbers = [*range(self.model.count)]
        random.shuffle(self.__numbers)

    def result(self) -> None:
        self.window.textEditExplanation.show()

    def setData(self, path: Path) -> None:
        self.model.path = path

    def nextQuestion(self) -> None:
        if self.__current < self.model.count:
            self.__current += 1
            self.setQuestion(self.__current)

        if self.__current > 0:
            self.window.pushButtonPrev.setEnabled(True)

        if self.__current == self.model.count - 1:
            self.window.pushButtonNext.setEnabled(False)
        else:
            self.window.pushButtonNext.setEnabled(True)

    def prevQuestion(self) -> None:
        if self.__current <= self.model.count \
            and self.__current > -1:
            self.__current -= 1
            self.setQuestion(self.__current)

        if self.__current != self.model.count:
            self.window.pushButtonNext.setEnabled(True)

        if self.__current == 0:
            self.window.pushButtonPrev.setEnabled(False)
        else:
            self.window.pushButtonPrev.setEnabled(True)

    def setQuestion(self, num: int) -> None:
        self.model.num = num
        self.window.labelQuestion.setText(self.model.question)
        for num, selection in enumerate(self.model.selections):
            eval(f"self.window.radioButton_{num}.setText('{selection}')")
        self.window.textEditExplanation.setPlainText(f"{self.model.en}\n{self.model.jp}\n\n{self.model.explanation}")
        self.window.textEditExplanation.hide()


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    ex = Connect()
    ex.window.show()
    sys.exit(app.exec_())


main()
