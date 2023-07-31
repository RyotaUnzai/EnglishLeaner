import random
import textwrap
import os
import sys
from datetime import date
from pathlib import Path

from PySide2 import QtWidgets, QtCore

from model.questions import Questions
from view.questions_view import Questions_Window


os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
QSS_PATH = Path(__file__).parent / "view" / "questions_view.qss"
RESOURCE_PATH = Path(__file__).parent.with_name("resource").absolute()


class Connect:
    __numbers: list = []
    __current: int = 0

    def __init__(self) -> None:
        self.window = Questions_Window()
        self.model = Questions(RESOURCE_PATH / "question_001.json")
        self.window.setStyleSheet(self.__loadQSS())
        # print(self.model.items)
        # self._setUI()
        self.__setNumbers()
        self.window.menu.pushButtonSelection.clicked.connect(self._setSelectionUI)
        self.window.menu.pushButtonSort.clicked.connect(self._setSortUI)

    def _setSortUI(self) -> None:
        self.__setSortQuestion(self.__numbers[self.__current])
        self.window.sort.lineEditAnswer.returnPressed.connect(self.__sortResult)
        self.window.sort.pushButtonNext.clicked.connect(self.__nextSortQuestion)
        self.window.sort.pushButtonPrev.clicked.connect(self.__prevSortQuestion)

    def _setSelectionUI(self) -> None:
        self.__setSelectionQuestion(self.__numbers[self.__current])
        self.window.selection.lineEditAnswer.returnPressed.connect(self.__selectionResult)
        self.window.selection.pushButtonNext.clicked.connect(self.__nextSelectionQuestion)
        self.window.selection.pushButtonPrev.clicked.connect(self.__prevSelectionQuestion)

    def insert_newlines(self, string, every=60):
        lines = ""
        newlines = []
        print(string)

        for i in range(0, len(lines), every):
            newlines.append(lines[i:i+every])

        return "\n".join(newlines)

    def __setSortQuestion(self, num: int) -> None:
        self.model.num = num
        self.window.sort.labelCount.setText(f"{self.model.count}")
        self.window.sort.labelJapanese.setText(self.model.jp)
        words = self.model.en.replace(".", "").split(" ")
        random.shuffle(words)
        numbered_words = [f"{i+1}.{word},  " for i, word in enumerate(words)]
        shuffled_text = " ".join(numbered_words)
        formatted_text = "\n".join(textwrap.wrap(shuffled_text, width=60))
        formatted_text = f"{formatted_text.replace('.', '. ')}"[:-1]

        self.window.sort.labelQuestion.setText(formatted_text)
        self.window.sort.labelCurrentNumber.setText(f"{self.__current+1} / {self.model.item_count}")
        self.window.sort.textEditExplanation.setPlainText(
            f"{self.model.en}\n{self.model.jp}\n\n{self.model.explanation}")
        self.window.sort.labelResult.setText(self.model.selections[self.model.answer])
        self.window.sort.textEditExplanation.hide()
        self.window.sort.labelResult.hide()

    def __setSelectionQuestion(self, num: int) -> None:
        self.model.num = num
        self.window.selection.labelCount.setText(f"{self.model.count}")
        self.window.selection.labelJapanese.setText(self.model.jp)
        self.window.selection.labelQuestion.setText(self.model.question)
        self.window.selection.labelCurrentNumber.setText(f"{self.__current+1} / {self.model.item_count}")
        for num, selection in enumerate(self.model.selections):
            eval(f"self.window.selection.radioButton_{num}.setText('{selection}')")
        self.window.selection.textEditExplanation.setPlainText(
            f"{self.model.en}\n{self.model.jp}\n\n{self.model.explanation}")
        self.window.selection.labelResult.setText(self.model.selections[self.model.answer])
        self.window.selection.textEditExplanation.hide()
        self.window.selection.labelResult.hide()

    def __loadQSS(self) -> str:
        with open(QSS_PATH.absolute().as_posix(), encoding="utf-8") as f:
            return f.read()

    def __setNumbers(self) -> None:
        self.__numbers = [*range(self.model.item_count)]
        random.shuffle(self.__numbers)

    def __sortResult(self) -> None:
        self.window.sort.textEditExplanation.show()
        self.window.sort.labelResult.show()
        self.window.setStyleSheet(self.__resultSortStyleSheet())

    def __resultSortStyleSheet(self) -> str:
        self.model.datetime = date.today().isoformat()
        if self.model.en == self.window.sort.lineEditAnswer.text():
            self.model.count += 1
            return self.__loadQSS() + "\nQLineEdit#lineEditAnswer{color: #38A46E;}"

        if self.model.count > 0:
            self.model.count -= 1

        return self.__loadQSS() + "\nQLineEdit#lineEditAnswer{color: #E01450;}"

    def __selectionResult(self) -> None:
        isChecked: bool = False
        self.window.selection.textEditExplanation.show()
        self.window.selection.labelResult.show()
        count = 0
        while count:
            exec(f"locals()['result'] = self.window.selection.radioButton_{count}.isChecked()")
            if locals()['result']:
                isChecked = True
                break
            if count <= 4:
                break
            count += 1
        if not isChecked:
            try:
                num = self.model.selections.index(self.window.selection.lineEditAnswer.text())
                eval(f"self.window.selection.radioButton_{num}.setChecked(True)")
            except ValueError:
                pass
        self.window.setStyleSheet(self.__resultSelectionStyleSheet())

    def __resultSelectionStyleSheet(self) -> str:
        exec(f"locals()['result'] = self.window.selection.radioButton_{self.model.answer}.isChecked()")
        self.model.datetime = date.today().isoformat()
        if locals()['result']:
            self.model.count += 1
            return self.__loadQSS() + f"\nQRadioButton#radioButton_{self.model.answer}{{color: #38A46E;}}"

        if self.model.count > 0:
            self.model.count -= 1

        return self.__loadQSS() + f"\nQRadioButton#radioButton_{self.model.answer}{{color: #E01450;}}"

    def __setData(self, path: Path) -> None:
        self.model.path = path

    def __initSortUI(self) -> None:
        pass

    def __initSelectionUI(self) -> None:
        self.window.buttonGroup.setExclusive(False)
        for num in range(4):
            exec(f"self.window.selection.radioButton_{num}.setChecked(False)")
        self.window.buttonGroup.setExclusive(True)
        self.window.selection.lineEditAnswer.setText("")

    def __nextSortQuestion(self) -> None:
        self.window.setStyleSheet(self.__loadQSS())
        self.__initSortUI()
        if self.__current < self.model.item_count:
            self.__current += 1
            self.__setSortQuestion(self.__numbers[self.__current])

        if self.__current > 0:
            self.window.sort.pushButtonPrev.setEnabled(True)

        if self.__current == self.model.item_count - 1:
            self.window.sort.pushButtonNext.setEnabled(False)
        else:
            self.window.sort.pushButtonNext.setEnabled(True)

    def __prevSortQuestion(self) -> None:
        self.window.setStyleSheet(self.__loadQSS())
        self.__initSortUI()
        if self.__current <= self.model.item_count \
                and self.__current > -1:
            self.__current -= 1
            self.__setSortQuestion(self.__numbers[self.__current])

        if self.__current != self.model.item_count:
            self.window.sort.pushButtonNext.setEnabled(True)

        if self.__current == 0:
            self.window.sort.pushButtonPrev.setEnabled(False)
        else:
            self.window.sort.pushButtonPrev.setEnabled(True)

    def __nextSelectionQuestion(self) -> None:
        self.window.setStyleSheet(self.__loadQSS())
        self.__initSelectionUI()
        if self.__current < self.model.item_count:
            self.__current += 1
            self.__setSelectionQuestion(self.__numbers[self.__current])

        if self.__current > 0:
            self.window.selection.pushButtonPrev.setEnabled(True)

        if self.__current == self.model.item_count - 1:
            self.window.selection.pushButtonNext.setEnabled(False)
        else:
            self.window.selection.pushButtonNext.setEnabled(True)

    def __prevSelectionQuestion(self) -> None:
        self.window.setStyleSheet(self.__loadQSS())
        self.__initSelectionUI()
        if self.__current <= self.model.item_count \
                and self.__current > -1:
            self.__current -= 1
            self.__setSelectionQuestion(self.__numbers[self.__current])

        if self.__current != self.model.item_count:
            self.window.selection.pushButtonNext.setEnabled(True)

        if self.__current == 0:
            self.window.selection.pushButtonPrev.setEnabled(False)
        else:
            self.window.selection.pushButtonPrev.setEnabled(True)

def main() -> None:
    app = QtWidgets.QApplication([])
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    ex = Connect()
    ex.window.show()
    sys.exit(app.exec_())


main()
