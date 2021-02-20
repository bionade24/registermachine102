from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5 import QtCore


class RegisterItem(QStandardItem):

    def __init__(self, row_nr, *args, **kwargs):
        super(RegisterItem, self).__init__(*args, **kwargs)
        self.setEditable(False)
        self.value = 0
        self.row_nr = row_nr

    def data(self, role):
        if role == QtCore.Qt.DisplayRole:
            return f"Register {self.row_nr}:    {self.value}"
        return QStandardItem.data(self, role)


class RegisterItemModel(QStandardItemModel):

    def __init__(self, *args, **kwargs):
        super(RegisterItemModel, self).__init__(*args, **kwargs)
        self.regCount = 0

