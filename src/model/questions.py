from pathlib import Path
from typing import Union
import json


class QuestionItemModel:
    __data: dict = {}

    def __init__(self, data):
        self.__data = data

    @property
    def question(self):
        return self.__data["question"]

    @property
    def selections(self):
        return self.__data["selections"]

    @property
    def answer(self):
        return self.__data["answer"]

    @property
    def explanation(self):
        return self.__data["explanation"]

    @property
    def en(self):
        return self.__data["en"]

    @property
    def jp(self):
        return self.__data["jp"]


class QuestionItemModels:
    __items: list[QuestionItemModel] = []
    __path: Path

    def __init__(self, path):
        self.clear()
        self.path = path
        self.setItem()

    @property
    def items(self) -> list[QuestionItemModel]:
        return self.__items

    def clear(self):
        self.__items.clear()

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, path: Union[str, Path]):
        if isinstance(path, Path):
            path = path.as_posix()
        with open(path) as f:
            self.__rawdata = json.load(f)

    def setItem(self):
        for data in self.__rawdata:
            self.__items.append(QuestionItemModel(data))


class Questions:
    __path = ""
    __model: QuestionItemModels

    def __init__(self, path):
        self.__model = QuestionItemModels(path)

    @property
    def model(self):
        return self.__model

    @property
    def path(self):
        return self.__model.path

    @path.setter
    def path(self, path):
        self.__model.path = path

    @property
    def items(self) -> list[QuestionItemModel]:
        return self.__model.items

    def Question(self, num) -> str:
        text = self.model.items[num].question
        text += "\n"
        for num, word in enumerate(self.model.items[num].selections):
            text += f"    {num}. {word}\n"
        return text
