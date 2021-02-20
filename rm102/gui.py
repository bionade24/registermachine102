from pathlib import Path
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtGui import QStandardItemModel, QBrush, QColorConstants
from PyQt5 import QtCore
from rm102.mainwindow import Ui_MainWindow
from rm102.command_register import CommandRegisterList, CommandRegisterItem
from rm102.register import RegisterItem, RegisterItemModel


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("RegisterMachine 102")
        self.regListModel = RegisterItemModel()
        self.commandRegisterList = CommandRegisterList(self.centralwidget)
        self.reglistView.setModel(self.regListModel)
        self.regListModel.appendRow(RegisterItem(1))
        self.lcdNumCmdReg.display(1)
        self.runButton.clicked.connect(self.runButtonClicked)
        self.stepButton.clicked.connect(self.stepButtonClicked)
        self.resetButton.clicked.connect(self.reset)
        self.loadButton.clicked.connect(self.loadButtonClicked)
        self.saveButton.clicked.connect(self.saveButtonClicked)
        self.commandRegisterList.model.update_gui.connect(self.update_gui)
        self.show()

    @QtCore.pyqtSlot(int, int, bool, name="update_gui")
    def update_gui(self, reg_count, acc, error):
        self.lcdNumAcc.display(acc)
        self.lcdNumCmdReg.display(reg_count + 1)
        self.commandRegisterList.model.item(reg_count).setBackground(
                QBrush(QColorConstants.Red if error else QColorConstants.Blue))

    def runButtonClicked(self):
        self.commandRegisterList.model.run(self.regListModel)

    def stepButtonClicked(self):
        self.commandRegisterList.model.step(self.lcdNumCmdReg.intValue() - 1,
                                            self.regListModel)

    def reset(self):
        self.commandRegisterList.model.accu = 0
        self.lcdNumAcc.display(0)
        self.lcdNumCmdReg.display(1)
        for i in range(0, self.commandRegisterList.model.rowCount()-1):
            self.commandRegisterList.model.item(i).setBackground(QBrush())
        for i in range(0, self.regListModel.rowCount()):
            self.regListModel.item(i).value = 0
        # TODO: Delete registers ?

    def loadButtonClicked(self):
        self.reset()
        fname = QFileDialog.getOpenFileName(
                self, 'Open file', str(Path.home()), "rm102 files (*.rm102)")
        with open(fname[0], 'r') as fobj:
            i = 0
            for line in fobj.readlines():
                self.commandRegisterList.model.item(i).setText(line)
                i += 1
                self.commandRegisterList.model.appendRow(
                        CommandRegisterItem(""))

    def saveButtonClicked(self):
        fname = QFileDialog.getSaveFileName(
                self, 'Save file', str(Path.home()), "rm102 files (*.rm102)")
        if not fname[0].endswith('.rm102'):
            fname = fname[0] + '.rm102'
        else:
            fname = fname[0]
        with open(fname, 'w') as fobj:
            for i in range(0, self.commandRegisterList.model.rowCount()-1):
                fobj.write(self.commandRegisterList.model.item(i).text()
                           + '\n')


def main(argv=None):
    app = QApplication(argv)
    main = MainWindow()
    main.show()
    app.exec_()


if __name__ == "__main__":
    main()
