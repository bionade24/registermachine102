from pathlib import Path
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QDialog, \
    QMessageBox
from PyQt5.QtGui import QBrush, QColorConstants, QPalette
from PyQt5 import QtCore
from rm102.mainwindow import Ui_MainWindow
from rm102.help_dialog import Ui_Dialog
from rm102.command_register import CommandRegisterList, CommandRegisterItem
from rm102.register import RegisterItem, RegisterItemModel


class HelpDialog(QDialog, Ui_Dialog):

    def __init__(self, *args, **kwargs):
        super(HelpDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("RegisterMachine 102 - Hilfe")


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
        self.saveUnderButton.clicked.connect(self.saveUnderButtonClicked)
        self.helpButton.clicked.connect(lambda: HelpDialog(self).show())
        self.commandRegisterList.model.update_gui.connect(self.update_gui)
        self.commandRegisterList.model.cells_changed.connect(
                lambda: self.file_is_open(self.filepath, False))
        self.commandRegisterList.model.itemChanged.connect(
                lambda: self.file_is_open(self.filepath, False))
        self.file_is_open(None, True)
        self.show()

    @QtCore.pyqtSlot(int, int, bool, name="update_gui")
    def update_gui(self, reg_count, acc, error):
        self.lcdNumAcc.display(acc)
        self.lcdNumCmdReg.display(reg_count + 1)
        try:
            self.commandRegisterList.model.item(reg_count).setBackground(
                    QBrush(QColorConstants.Red if error else QColorConstants.Blue))
        except AttributeError:
            self.commandRegisterList.model.appendRow(CommandRegisterItem(""))
            self.commandRegisterList.model.item(reg_count).setBackground(
                    QBrush(QColorConstants.Red if error else QColorConstants.Red))

    def runButtonClicked(self):
        self.commandRegisterList.model.run(self.regListModel)
        if self.commandRegisterList.model.stop is not None:
            self.runButton.setEnabled(False)

    def closeEvent(self, event):
        if not self.changes_saved:
            filename = filename = self.filepath.split('/')[-1] if self.filepath else 'Unbenannt'
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Änderungen speichern?")
            msg.setText(
                f"Sollen die Änderungen an {filename} gespeichert werden?")
            msg.setStandardButtons(
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            msg.setEscapeButton(QMessageBox.Cancel)
            result = msg.exec()

            if result == QMessageBox.Cancel:
                event.ignore()
            elif result == QMessageBox.Save:
                self.saveButtonClicked()
                event.accept()
            else:
                event.accept()

    def stepButtonClicked(self):
        self.commandRegisterList.model.step(self.lcdNumCmdReg.intValue() - 1,
                                            self.regListModel)

    def reset(self, remove_stopper=False):
        self.commandRegisterList.model.accu = 0
        self.lcdNumAcc.display(0)
        self.lcdNumCmdReg.display(1)
        self.runButton.setEnabled(True)
        for i in range(0, self.commandRegisterList.model.rowCount()):
            self.commandRegisterList.model.item(i).setBackground(QBrush())
        for i in range(1, self.regListModel.rowCount()):
            self.regListModel.takeRow(1)
        self.regListModel.item(0).setValue(0)
        if remove_stopper:
            cmd_mod = self.commandRegisterList.model
            if cmd_mod.stop is not None:
                cmd_mod.item(cmd_mod.stop).setForeground(QPalette().text())
                cmd_mod.stop = None

    def loadButtonClicked(self):
        self.reset(remove_stopper=True)
        fname = QFileDialog.getOpenFileName(
                self, 'Open file', str(Path.home()), "rm102 files (*.rm102)")
        if fname[0] == '':
            return
        with open(fname[0], 'r') as fobj:
            i = 0
            for line in fobj.readlines():
                self.commandRegisterList.model.item(i).setText(line.strip('\n'))
                i += 1
                if self.commandRegisterList.model.item(i) is None:
                    self.commandRegisterList.model.appendRow(
                            CommandRegisterItem(""))
        self.file_is_open(fname[0], True)

    def saveButtonClicked(self):
        if self.filepath is None:
            fname = QFileDialog.getSaveFileName(
                self, 'Save file', str(Path.home()), "rm102 files (*.rm102)")
        else:
            fname = [self.filepath]
        if fname[0] == '':
            return
        if not fname[0].endswith('.rm102'):
            fname = fname[0] + '.rm102'
        else:
            fname = fname[0]
        with open(fname, 'w') as fobj:
            for i in range(0, self.commandRegisterList.model.rowCount()):
                if self.commandRegisterList.model.item(i).text() != '':
                    fobj.write(self.commandRegisterList.model.item(i).text().strip('\n')
                               + '\n')
        self.file_is_open(fname, True)

    def saveUnderButtonClicked(self):
        self.filepath = None
        self.saveButtonClicked()

    def file_is_open(self, path, saved):
        self.filepath = path
        self.changes_saved = saved

        prefix = '' if saved else '*'
        filename = self.filepath.split('/')[-1] if self.filepath \
          else 'Unbenannt'
        self.setWindowTitle(f"RegisterMachine 102 - {prefix}{filename}")


def main(argv=None):
    app = QApplication(argv)
    main = MainWindow()
    main.show()
    app.exec_()


if __name__ == "__main__":
    main()
