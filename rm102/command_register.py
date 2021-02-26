from enum import IntEnum
from PyQt5.QtGui import QStandardItem, QFont, QStandardItemModel, \
        QBrush, QColorConstants, QPalette
from PyQt5.QtWidgets import QTableView
from PyQt5 import QtCore
from rm102.register import RegisterItem


class CMD(IntEnum):
    ACC = 0
    STORE = 1
    JMP = 2


class CommandRegisterItemModel(QStandardItemModel):

    command_dict = {
            "LOAD": lambda val, acc, reg: (CMD.ACC, reg),
            "DLOAD": lambda val, acc, reg: (CMD.ACC, val),
            "STORE": lambda val, acc, reg: (CMD.STORE, val),
            "ADD": lambda val, acc, reg: (CMD.ACC, acc + reg),
            "SUB": lambda val, acc, reg: (CMD.ACC, acc - reg),
            "MULT": lambda val, acc, reg: (CMD.ACC, acc * reg),
            "DIV": lambda val, acc, reg: (CMD.ACC, acc // reg),
            "JUMP": lambda val, acc, reg: (CMD.JMP, val),
            "JGE": lambda val, acc, reg: (CMD.JMP, val) if acc >= 0 else (
                None, None),
            "JGT": lambda val, acc, reg: (CMD.JMP, val) if acc > 0 else (
                None, None),
            "JLE": lambda val, acc, reg: (CMD.JMP, val) if acc <= 0 else (
                None, None),
            "JLT": lambda val, acc, reg: (CMD.JMP, val) if acc < 0 else (
                None, None),
            "JEQ": lambda val, acc, reg: (CMD.JMP, val) if acc == 0 else (
                None, None),
            "JNE": lambda val, acc, reg: (CMD.JMP, val) if acc != 0 else (
                None, None)
    }

    update_gui = QtCore.pyqtSignal(int, int, bool)

    def __init__(self, *args, **kwargs):
        super(CommandRegisterItemModel, self).__init__(*args, **kwargs)
        self.accu = 0
        self.stop = None

    def exec(self, cmd_reg_row, registerList, run_all=False):
        cmd_reg_row_next = None
        command = self.item(cmd_reg_row).text().strip('\n').split(' ')
        # Special case for END
        if command[0] == "END":
            self.update_gui.emit(cmd_reg_row, self.accu, False)
            return
        # All other cases
        try:
            cmd, res = self.command_dict[command[0]](
                    int(command[1]), self.accu, self.check_for_register(
                        command[0], int(command[1]), registerList))
            if cmd == CMD.ACC:
                self.accu = res
            elif cmd == CMD.STORE:
                registerList.item(res - 1).setValue(self.accu)
            elif cmd == CMD.JMP:
                cmd_reg_row_next = res - 1
        except BaseException:
            self.update_gui.emit(cmd_reg_row, self.accu, True)
            return
        if not cmd_reg_row_next:
            cmd_reg_row_next = cmd_reg_row + 1
        if run_all and cmd_reg_row_next < self.rowCount() and \
           (self.stop is None or self.stop >= cmd_reg_row_next):
            self.exec(cmd_reg_row_next, registerList, run_all)
        else:
            self.update_gui.emit(cmd_reg_row_next, self.accu,
                                 True if run_all and self.stop is None else False)
            self.item(cmd_reg_row).setBackground(QBrush())

    def check_for_register(self, cmd, val, registerList):
        reg = registerList.item(val - 1)
        if type(reg) is RegisterItem:
            return reg.value()
        else:
            if cmd == 'STORE':
                for i in range(registerList.rowCount(), val):
                    registerList.appendRow(RegisterItem(i + 1))
            return 0

    @QtCore.pyqtSlot(int, QStandardItemModel, name="step")
    def step(self, cmd_reg_row, registerList):
        self.exec(cmd_reg_row, registerList)

    @QtCore.pyqtSlot(QStandardItemModel, name="run")
    def run(self, registerList):
        self.exec(0, registerList, True)


class CommandRegisterItem(QStandardItem):

    def __init__(self, *args, **kwargs):

        super(CommandRegisterItem, self).__init__(*args, **kwargs)
        font = QFont()
        font.setCapitalization(QFont.AllUppercase)
        self.setFont(font)

    def setData(self, value, role=QtCore.Qt.UserRole + 1):
        if role == QtCore.Qt.EditRole:
            value = str(value).strip(' ').upper()
            self.emitDataChanged()
        return QStandardItem.setData(self, value, role)


class CommandRegisterList(QTableView):

    def __init__(self, *args, **kwargs):
        super(CommandRegisterList, self).__init__(*args, **kwargs)
        self.setShowGrid(False)
        self.move(10, 10)
        # TODO: What to do on smaller screen areas
        # Without explicit width, the column won't align the TableView
        self.setMinimumSize(285, 531)
        self.model = CommandRegisterItemModel(self)
        self.model.appendRow(CommandRegisterItem(""))
        self.model.setHorizontalHeaderLabels(["Befehle"])
        self.setModel(self.model)
        self.setColumnWidth(0, self.width())

    def keyPressEvent(self, event):
        try:
            index = self.selectedIndexes()[0]
        except IndexError:
            index = self.model.index(0, 0)
        if event.key() == QtCore.Qt.Key_Return:
            self.model.insertRow(index.row() + 1, CommandRegisterItem())
            self.setCurrentIndex(self.model.index(index.row() + 1, 0))
        elif event.key() == QtCore.Qt.Key_Insert:
            self.model.insertRow(index.row(), CommandRegisterItem())
            self.setCurrentIndex(self.model.index(index.row(), 0))
        elif event.key() == QtCore.Qt.Key_Delete:
            if index.row() != 0:
                self.model.takeRow(index.row())
                self.setCurrentIndex(self.model.index(index.row() - 1, 0))
        elif event.key() == QtCore.Qt.Key_Left or event.key() == QtCore.Qt.Key_Right:
            self.edit(index)
        super(QTableView, self).keyPressEvent(event)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            index = self.indexAt(event.localPos().toPoint())
            if index.row() >= 0:
                # Explicitly allow 0
                if self.model.stop is not None:
                    self.model.item(self.model.stop).setForeground(
                            QPalette().text())
                    if self.model.stop == index.row():
                        self.model.stop = None
                        return
                self.model.stop = index.row()
                self.model.itemFromIndex(index).setForeground(
                        QBrush(QColorConstants.Yellow))
        super(QTableView, self).mousePressEvent(event)

