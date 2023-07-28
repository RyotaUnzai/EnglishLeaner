import json
from pathlib import Path
from typing import Union


class QuestionItemModel:
    __data: dict = {}

    def __init__(self, data: dict) -> None:
        self.__data = data

    @property
    def question(self) -> str:
        return self.__data["question"]

    @property
    def selections(self) -> list[str]:
        return self.__data["selections"]

    @property
    def answer(self) -> int:
        return self.__data["answer"]

    @property
    def explanation(self) -> str:
        return self.__data["explanation"]

    @property
    def en(self) -> str:
        return self.__data["en"]

    @property
    def jp(self) -> str:
        return self.__data["jp"]


class QuestionItemModels:
    __items: list[QuestionItemModel] = []
    __path: Path

    def __init__(self, path: Path) -> None:
        self.clear()
        self.path = path
        self.setItem()

    @property
    def items(self) -> list[QuestionItemModel]:
        return self.__items

    def clear(self) -> None:
        self.__items.clear()

    @property
    def path(self) -> Path:
        return self.__path

    @path.setter
    def path(self, path: Union[str, Path]) -> None:
        if isinstance(path, Path):
            path = path.as_posix()
        with open(path, encoding="utf-8") as f:
            self.__rawdata = json.load(f)

    def setItem(self) -> None:
        for data in self.__rawdata:
            self.__items.append(QuestionItemModel(data))


class Questions:
    __path = ""
    __model: QuestionItemModels
    __num: int = 0

    def __init__(self, path) -> None:
        self.__model = QuestionItemModels(path)

    @property
    def count(self) -> int:
        return len(self.items)

    @property
    def num(self) -> int:
        return self.__num

    @num.setter
    def num(self, number: int) -> None:
        self.__num = number

    @property
    def item(self) -> QuestionItemModel:
        return self.items[self.num]

    @property
    def model(self) -> QuestionItemModels:
        return self.__model

    @property
    def path(self) -> Path:
        return self.__model.path

    @path.setter
    def path(self, path: Path) -> None:
        self.__model.path = path

    @property
    def items(self) -> list[QuestionItemModel]:
        return self.__model.items

    @property
    def question(self) -> str:
        return self.item.question

    @property
    def selections(self) -> list[str]:
        return self.item.selections

    @property
    def answer(self) -> int:
        return self.item.answer

    @property
    def explanation(self) -> str:
        return self.item.explanation

    @property
    def en(self) -> str:
        return self.item.en

    @property
    def jp(self) -> str:
        return self.item.jp
