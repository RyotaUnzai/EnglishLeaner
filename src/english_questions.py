import random
import os
import sys
from datetime import date
from pathlib import Path

from PySide2 import QtWidgets, QtCore

from model.questions import Questions
from model.sortlistmodel import SortItemModel
from view.questions_view import Questions_Window


os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
QSS_PATH = Path(__file__).parent / "view" / "questions_view.qss"
RESOURCE_PATH = Path(__file__).parent.with_name("resource").absolute()


class Connect:
    __numbers: list = []
    __current: int = 0
    __sort_connected: bool = False
    __correct_color = "#38A46E"
    __wrong_color = "#E01450"

    @property
    def words(self) -> str:
        return self.model.en.replace(".", "").split(" ")

    @property
    def word_counts(self) -> int:
        return len(self.words)

    def __init__(self) -> None:
        self.window = Questions_Window()
        self.model = Questions(RESOURCE_PATH / "question_001.json")
        self.window.frame.selection.listView.setModel(self.model.sortListModel)
        self.window.setStyleSheet(self.__loadQSS())
        self.window.menu.pushButtonSelection.clicked.connect(self.__setUI)
        self.window.menu.pushButtonSort.clicked.connect(self.__setUI)
        self.window.menu.pushButtonWrite.clicked.connect(self.__setUI)
        self.window.menu.pushButtonExport.clicked.connect(self.__setUI)
        self.window.frame.lineEditAnswer.returnPressed.connect(self.__result)
        self.window.frame.pushButtonNext.clicked.connect(self.__nextQuestion)
        self.window.frame.pushButtonBack.clicked.connect(self.__reset)
        self.window.frame.pushButtonPrev.clicked.connect(self.__prevQuestion)
        self.window.actionOpen.triggered.connect(self.__open)
        self.window.nextQuestion.connect(self.__nextQuestion)
        self.window.prevQuestion.connect(self.__prevQuestion)

    def __loadQSS(self) -> str:
        with open(QSS_PATH.absolute().as_posix(), encoding="utf-8") as f:
            return f.read()

    def __reset(self) -> str:
        self.model.count = 0
        if self.__current == 0:
            self.window.frame.pushButtonPrev.setEnabled(False)
        else:
            self.window.frame.pushButtonPrev.setEnabled(True)

    def __open(self) -> None:
        fileDialog = QtWidgets.QFileDialog.getOpenFileNames(
            parent=self.window,
            caption="open json",
            dir=RESOURCE_PATH.as_posix(),
            filter="Json (*.json)"
        )
        self.model.path = Path(fileDialog[0][0])

    def __setNumbers(self) -> None:
        self.__numbers = [*range(self.model.item_count)]
        random.shuffle(self.__numbers)
        self.__current = 0

    def __setUI(self) -> None:
        self.__setNumbers()
        self.__setQuestion(self.__numbers[self.__current])
        if self.window.currentMode == "sort":
            self.__sort_connected = True
            self.window.frame.lineEditAnswer.textChanged.connect(
                self.__checkSentence
            )
        elif self.window.currentMode:
            if self.__sort_connected:
                self.window.frame.lineEditAnswer.textChanged.disconnect(
                    self.__checkSentence
                )
        if self.window.currentMode == "export":
            text = ""
            for item in self.model.items:
                text += f"{item.en}\n"
            self.window.frame.textEditExplanation.setPlainText(text)
            self.window.frame.frameExplanation.show()

    def __checkSentence(self, value: str) -> None:
        inputWords = value.replace(".", "").split(" ")
        for num, item in enumerate(self.model.sortListModel.items):
            try:
                inputWords.remove(item.name)
                self.model.sortListModel.setData(num, True)
            except Exception:
                self.model.sortListModel.setData(num, False)

    def __result(self) -> None:
        self.model.datetime = date.today().isoformat()
        self.window.frame.frameExplanation.show()
        self.window.setFocus()

        if self.window.currentMode == "selection":
            isChecked: bool = False
            count = 0
            while count:
                exec(
                    f"locals()['result'] = self.window.frame.selection.radioButton_{count}.isChecked()"
                )
                if locals()['result']:
                    isChecked = True
                    break
                if count <= 4:
                    break
                count += 1
            if not isChecked:
                try:
                    num = self.model.selections.index(self.window.frame.lineEditAnswer.text())
                    eval(f"self.window.frame.selection.radioButton_{num}.setChecked(True)")
                except ValueError:
                    pass

        self.window.setStyleSheet(self.__resultStyleSheet())

    def __resultStyleSheet(self) -> str:
        if self.window.currentMode == "sort":
            if self.model.en == self.window.frame.lineEditAnswer.text():
                self.model.count += 1
                return self.__loadQSS() + f"\nQLineEdit#lineEditAnswer{{color: {self.__correct_color};}}"

            if self.model.count > 0:
                self.model.count -= 1

            return self.__loadQSS() + f"\nQLineEdit#lineEditAnswer{{color: {self.__wrong_color};}}"
        elif self.window.currentMode == "write":
            if self.window.frame.lineEditAnswer.text() == self.model.selections[self.model.answer]:
                self.model.count += 1
                return self.__loadQSS() + f"\nQLineEdit#lineEditAnswer{{color: {self.__correct_color};}}"

            return self.__loadQSS() + f"\nQLineEdit#lineEditAnswer{{color: {self.__wrong_color};}}"

        elif self.window.currentMode == "selection":
            exec(
                f"locals()['result'] = self.window.frame.selection.radioButton_{self.model.answer}.isChecked()"
            )
            if locals()["result"]:
                self.model.count += 1
                return self.__loadQSS() \
                    + f"\nQRadioButton#radioButton_{self.model.answer}{{color: {self.__correct_color};}}"

            if self.model.count > 0:
                self.model.count -= 1

            return self.__loadQSS() \
                + f"\nQRadioButton#radioButton_{self.model.answer}{{color: {self.__wrong_color};}}"
        return self.__loadQSS()

    def __initUI(self) -> None:
        self.window.frame.lineEditAnswer.setText("")
        self.window.frame.lineEditAnswer.setFocus()
        if self.window.currentMode == "selection":
            self.window.frame.selection.buttonGroup.setExclusive(False)
            for num in range(4):
                exec(f"self.window.frame.selection.radioButton_{num}.setChecked(False)")
            self.window.frame.selection.buttonGroup.setExclusive(True)

    def __nextQuestion(self) -> None:
        self.window.setStyleSheet(self.__loadQSS())
        self.__initUI()
        if self.__current < self.model.item_count:
            self.__current += 1
            self.__setQuestion(self.__numbers[self.__current])

        if self.__current > 0:
            self.window.frame.pushButtonPrev.setEnabled(True)

        if self.__current == self.model.item_count - 1:
            self.window.frame.pushButtonNext.setEnabled(False)
        else:
            self.window.frame.pushButtonNext.setEnabled(True)

    def __prevQuestion(self) -> None:
        self.window.setStyleSheet(self.__loadQSS())
        self.__initUI()
        if self.__current <= self.model.item_count \
                and self.__current > -1:
            self.__current -= 1
            self.__setQuestion(self.__numbers[self.__current])

        if self.__current != self.model.item_count:
            self.window.frame.pushButtonNext.setEnabled(True)

        if self.__current == 0:
            self.window.frame.pushButtonPrev.setEnabled(False)
        else:
            self.window.frame.pushButtonPrev.setEnabled(True)

    def __setQuestion(self, num: int) -> None:
        self.model.num = num
        self.window.setStyleSheet(self.__loadQSS())
        self.window.frame.lineEditAnswer.setText("")
        self.window.frame.labelCount.setText(f"{self.model.count}")
        self.window.frame.selection.labelJapanese.setText(self.model.jp)

        if self.window.currentMode == "write" or self.window.currentMode == "selection":
            self.window.frame.selection.listView.hide()
            self.window.frame.selection.labelQuestion.setText(self.model.question)
            if self.window.currentMode == "selection":
                for num, selection in enumerate(self.model.selections):
                    eval(
                        f"self.window.frame.selection.radioButton_{num}.setText('{selection}')"
                    )

        elif self.window.currentMode == "export":
            self.window.frame.selection.listView.hide()
            self.window.frame.selection.labelQuestion.setText("")

        elif self.window.currentMode == "sort":
            self.window.frame.selection.listView.show()
            self.window.frame.selection.labelQuestion.setText("")
            words = self.model.en.replace(".", "").split(" ")
            random.shuffle(words)
            self.__count_word = len(words)
            self.numbered_words: list[str] = [f"{i+1}.{word},  " for i, word in enumerate(words)]
            if self.model.sortListModel.items != []:
                self.model.sortListModel.clear()
            for word in self.numbered_words:
                self.model.sortListModel.addItem(
                    SortItemModel(name=word.split(".")[1].replace(",  ", ""), displayName=word)
                )
            self.window.frame.selection.listView.show()
        self.window.frame.labelCurrentNumber.setText(f"{self.__current+1} / {self.model.item_count}")
        self.window.frame.textEditExplanation.setPlainText(
            f"{self.model.en}\n{self.model.jp}\n\n{self.model.explanation}"
        )
        self.window.frame.labelResult.setText(self.model.selections[self.model.answer])
        self.window.frame.frameExplanation.hide()


def main() -> None:
    app = QtWidgets.QApplication([])
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    ex = Connect()
    ex.window.show()
    sys.exit(app.exec_())


main()
