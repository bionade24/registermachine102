from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5 import QtCore


class RegisterItem(QStandardItem):

    def __init__(self, row_nr, *args, **kwargs):
        super(RegisterItem, self).__init__(*args, **kwargs)
        self.setEditable(False)
        self._value = 0
        self.row_nr = row_nr

    def data(self, role):
        if role == QtCore.Qt.DisplayRole:
            return f"Register {self.row_nr}:    {self._value}"
        return QStandardItem.data(self, role)

    def value(self):
        return self._value

    def setValue(self, val):
        self._value = val
        self.emitDataChanged()


class RegisterItemModel(QStandardItemModel):

    def __init__(self, *args, **kwargs):
        super(RegisterItemModel, self).__init__(*args, **kwargs)
        self.regCount = 0

