import random
import sys
from datetime import date
from pathlib import Path

from PySide2 import QtWidgets

from model.questions import PATH_LOCALAPPDATA, Questions
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
        self.__setNumbers()
        self._setUI()

    def _setUI(self) -> None:
        self.window.setStyleSheet(self.__loadQSS())
        self.window.lineEditAnswer.returnPressed.connect(self.__result)
        self.window.pushButtonNext.clicked.connect(self.__nextQuestion)
        self.window.pushButtonPrev.clicked.connect(self.__prevQuestion)
        
        self.window.labelCurrentNumber.setText(f"{self.__current} / {self.model.item_count}")

    def __loadQSS(self) -> str:
        with open(QSS_PATH.absolute().as_posix(), encoding="utf-8") as f:
            return f.read()

    def __setNumbers(self) -> None:
        self.__numbers = [*range(self.model.item_count)]
        random.shuffle(self.__numbers)
        self.__setQuestion(self.__numbers[self.__current])

    def __result(self) -> None:
        isChecked: bool = False
        self.window.textEditExplanation.show()
        self.window.labelResult.show()
        count = 0
        while count:
            exec(f"locals()['result'] = self.window.radioButton_{count}.isChecked()")
            if locals()['result']:
                isChecked = True
                break
            if count <= 4:
                break
            count += 1
        if not isChecked:
            try:
                num = self.model.selections.index(self.window.lineEditAnswer.text())
                eval(f"self.window.radioButton_{num}.setChecked(True)")
            except ValueError:
                pass
        self.window.setStyleSheet(self.__resultStyleSheet())

    def __resultStyleSheet(self) -> str:
        exec(f"locals()['result'] = self.window.radioButton_{self.model.answer}.isChecked()")
        self.model.datetime = date.today().isoformat()
        if locals()['result']:
            self.model.count += 1
            return self.__loadQSS() + f"\nQRadioButton#radioButton_{self.model.answer}{{color: #38A46E;}}"

        if self.model.count > 0:
            self.model.count -= 1

        return self.__loadQSS() + f"\nQRadioButton#radioButton_{self.model.answer}{{color: #E01450;}}"

    def __setData(self, path: Path) -> None:
        self.model.path = path

    def __initUI(self) -> None:
        self.window.buttonGroup.setExclusive(False)
        for num in range(4):
            exec(f"self.window.radioButton_{num}.setChecked(False)")
        self.window.buttonGroup.setExclusive(True)
        self.window.lineEditAnswer.setText("")

    def __nextQuestion(self) -> None:
        self.window.setStyleSheet(self.__loadQSS())
        self.__initUI()
        if self.__current < self.model.item_count:
            self.__current += 1
            self.__setQuestion(self.__numbers[self.__current])

        if self.__current > 0:
            self.window.pushButtonPrev.setEnabled(True)

        if self.__current == self.model.item_count - 1:
            self.window.pushButtonNext.setEnabled(False)
        else:
            self.window.pushButtonNext.setEnabled(True)

    def __prevQuestion(self) -> None:
        self.window.setStyleSheet(self.__loadQSS())
        self.__initUI()
        if self.__current <= self.model.item_count \
                and self.__current > -1:
            self.__current -= 1
            self.__setQuestion(self.__numbers[self.__current])

        if self.__current != self.model.item_count:
            self.window.pushButtonNext.setEnabled(True)

        if self.__current == 0:
            self.window.pushButtonPrev.setEnabled(False)
        else:
            self.window.pushButtonPrev.setEnabled(True)

    def __setQuestion(self, num: int) -> None:
        self.model.num = num
        self.window.labelCount.setText(f"{self.model.count}")
        self.window.labelQuestion.setText(self.model.question)
        self.window.labelCurrentNumber.setText(f"{self.__current} / {self.model.item_count}")
        for num, selection in enumerate(self.model.selections):
            eval(f"self.window.radioButton_{num}.setText('{selection}')")
        self.window.textEditExplanation.setPlainText(f"{self.model.en}\n{self.model.jp}\n\n{self.model.explanation}")
        self.window.labelResult.setText(self.model.selections[self.model.answer])
        self.window.textEditExplanation.hide()
        self.window.labelResult.hide()


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    ex = Connect()
    ex.window.show()
    sys.exit(app.exec_())


main()
