import json
import os
import shutil
from pathlib import Path
from typing import Union

PATH_LOCALAPPDATA = Path(f"{os.getenv('LOCALAPPDATA')}") / "EnglishLeaner"

if not PATH_LOCALAPPDATA.exists():
    PATH_LOCALAPPDATA.mkdir()


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

    @property
    def count(self) -> int:
        return self.__data["count"]

    @count.setter
    def count(self, count: int) -> None:
        self.__data["count"] = count

    @property
    def datetime(self) -> str:
        return self.__data["datetime"]

    @datetime.setter
    def datetime(self, datetime: str) -> None:
        self.__data["datetime"] = datetime


class QuestionItemModels:
    __items: list[QuestionItemModel] = []
    __path: Path

    def __init__(self, path: Path) -> None:
        self.clear()
        self.path = path
        self.setItem()
        self.save()

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
        if isinstance(path, str):
            path = Path(path)
        self.__path = path
        with open(self.__path, encoding="utf-8") as f:
            self.__rawdata = json.load(f)

        for data in self.__rawdata:
            if "count" not in data:
                data["count"] = 0
            if "datetime" not in data:
                data["datetime"] = ""

    def save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.__rawdata, f, indent=4)

    def setItem(self) -> None:
        for data in self.__rawdata:
            self.__items.append(QuestionItemModel(data))


class Questions:
    __path = ""
    __model: QuestionItemModels
    __num: int = 0

    def __init__(self, path: Union[Path, str]) -> None:
        if isinstance(path, str):
            path = Path(path)
        local_path = PATH_LOCALAPPDATA / path.name
        shutil.copyfile(path, local_path)
        self.__model = QuestionItemModels(local_path)

    @property
    def item_count(self) -> int:
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

    @property
    def count(self) -> int:
        return self.item.count

    @count.setter
    def count(self, count: int) -> None:
        self.item.count = count
        self.__model.save()

    @property
    def datetime(self) -> str:
        return self.item.datetime

    @datetime.setter
    def datetime(self, datetime: str) -> None:
        self.item.datetime = datetime
        self.__model.save()
