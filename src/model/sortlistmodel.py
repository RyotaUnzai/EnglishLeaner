from typing import Any, Union
from pydantic import BaseModel
from PySide2 import QtCore, QtGui

WORD_ROLE = QtCore.Qt.UserRole
WROTE_ROLE = QtCore.Qt.UserRole + 1


class SortItemModel(BaseModel):
    name: str
    displayName: str
    wrote: bool = False


class SortListModel(QtCore.QAbstractListModel):
    __items: list[SortItemModel]

    def __init__(self, parent: QtCore.QObject = None, data: list[SortItemModel] = []):
        super(SortListModel, self).__init__(parent)
        self.__items = data

    @property
    def items(self) -> list[SortItemModel]:
        return self.__items

    def addItem(self, item: SortItemModel) -> None:
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self.items.append(item)
        self.endInsertRows()

    def clear(self) -> None:
        self.items.clear()

    def rowCount(self, parent: QtCore.QModelIndex = None) -> int:
        return len(self.__items)

    def data(self, index: QtCore.QModelIndex, role: int = QtCore.Qt.DisplayRole) -> Union[Any, None]:
        item: SortItemModel = self.items[index.row()]
        if not index.isValid():
            return None

        if not 0 <= index.row() < len(self.items):
            return None

        if role == int(QtCore.Qt.DisplayRole):
            return item.displayName
        elif role == int(QtCore.Qt.ForegroundRole):
            if item.wrote:
                return QtGui.QColor("#022")
        elif role == WORD_ROLE:
            return item.name
        else:
            return None
        return None

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        return QtCore.Qt.NoItemFlags

    def setData(self, index: Union[QtCore.QModelIndex, int], value: Any, role: int = WROTE_ROLE) -> bool:
        if role == WROTE_ROLE:
            self.items[index].wrote = value
            self.dataChanged.emit(index, index)
            return True
        return False
