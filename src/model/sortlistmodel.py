
from PySide2 import QtCore
from typing import Union
from pydantic import BaseModel


WORD_ROLE = QtCore.Qt.UserRole


class SortItemModel(BaseModel):
    name: str
    displayName: str


class SortListModel(QtCore.QAbstractListModel):
    __items: list[SortItemModel]

    def __init__(self, parent=None, data: list[SortItemModel] = []):
        super(SortListModel, self).__init__(parent)
        self.items = data

    @property
    def items(self) -> list[SortItemModel]:
        return self.__items

    @items.setter
    def items(self, items: list[SortItemModel]) -> None:
        self.__items = items

    def addItem(self, item: SortItemModel) -> None:
        self.items.append(item)

    def clear(self) -> None:
        self.items.clear()

    def rowCount(self, parent=QtCore.QModelIndex()) -> int:
        return len(self.items)

    def data(self, index, role=QtCore.Qt.DisplayRole) -> Union[str, None]:
        item: SortItemModel = self.items[index.row()]
        if not index.isValid():
            return None

        if not 0 <= index.row() < len(self.items):
            return None

        if role == QtCore.Qt.DisplayRole:
            return item.name
        elif role == WORD_ROLE:
            return item.displayName
        else:
            return None

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
