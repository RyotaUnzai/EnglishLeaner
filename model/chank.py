from pathlib import Path
import openpyxl
from openpyxl.workbook import Workbook
import random


class chankClass:
    _code: str
    currentDir = Path(__file__).resolve().parent
    xlDir = Path(currentDir.parent, "xl")
    resultDir = Path(currentDir.parent, "result")
    _wbName: str
    _wb: Workbook
    symbols = [".", ","]
    _ratio = 30

    def load(self):
        self._wb = openpyxl.load_workbook(self.wbFilePath)

    @property
    def ratio(self) -> int:
        return self._ratio

    @ratio.setter
    def ratio(self, value: int):
        if value > 100:
            self._ratio = 100
        elif value < 0:
            self._ratio = 0
        else:
            self._ratio = value

    @property
    def wb(self) -> Workbook:
        return self._wb

    @property
    def wbFilePath(self) -> str:
        return Path(self.xlDir, self.wbName)

    @property
    def code(self) -> str:
        return self._code

    @code.setter
    def code(self, value: str):
        self._code = value

    @property
    def wbName(self) -> str:
        return f"{self._wbName}.xlsx"

    @wbName.setter
    def wbName(self, value: str):
        self._wbName = value

    @property
    def sheet(self) -> str:
        return self.wb[self.wb.sheetnames[0]]

    def getLists(self):
        return ([[cell.value for cell in row] for row in self.sheet])

    def setSpoiler(self, textA, textB, textC):
        return f"""
{textA}
:::spoiler {textB}
{textC}
:::"""

    def addParentheses(self, words):
        en = ""

        if self.ratio != 100:
            wordNum = (int(len(words) * (self.ratio / 100)))
            num = int(random.uniform(0, wordNum))
        else:
            num = len(words)

        count = 0
        for word in words:
            inputWord = word

            if word[-1] in self.symbols:
                text = f"( ){word[-1]} "

            elif '"' in word or '“' in word or '”' in word:
                if '“' in word or '”' in word:
                    wordlist = []
                    tempList = word.split('“')
                    for w in tempList:
                        wordlist += w.split('”')
                else:
                    wordlist = word.split('"')
                text = ""
                for w in wordlist:
                    if w == "":
                        text += '"'
                        continue
                    inputWord = w
                    text += "( )"
                text = f"{text} "
            else:
                text = f"{word} "

            if self.ratio == 100:
                en += text
                continue
            if count == int(num/2):
                en += text.replace("( )", inputWord)
                count += 1
                continue
            elif num != 0:
                if not bool(random.getrandbits(1)):
                    en += text.replace("( )", inputWord)
                    continue
                en += text
                count += 1
                continue
            else:
                en += text
                count += 1
        return en[:-1]

    def allParentheses(self, words):
        en = ""
        for word in words:
            if word[-1] in self.symbols:
                en += f"( ){word[-1]} "
                continue
            elif '"' in word or '“' in word or '”' in word:
                if '“' in word or '”' in word:
                    wordlist = []
                    tempList = word.split('“')
                    for w in tempList:
                        wordlist += w.split('”')
                else:
                    wordlist = word.split('"')
                text = ""
                for w in wordlist:
                    if w == "":
                        text += '"'
                        continue
                    text += "( )"
                en += f"{text} "
                continue
            en += "( ) "
        return en[:-1]

    def createCode(self, mode: int = 0):
        self.code = ""
        for e, j in self.getLists():
            if mode == 0:
                self.code += self.setSpoiler(e, j)
                continue
            words = e.split()
            if mode == 1:
                en = self.allParentheses(words)
            if mode == 2:
                en = self.addParentheses(words)

            self.code += self.setSpoiler(en, j, e)

        self.save()

    def save(self):
        with open(
            Path(self.resultDir, self.wbName).as_posix().replace(
                ".xlsx", ".txt"), mode='w', encoding="shift_jis"
        ) as f:
            f.write(self.code)


chank = chankClass()
chank.wbName = "test"
chank.load()

chank.createCode(mode=1)
