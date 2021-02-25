# -*- Makefile -*-

all:
	python3 -m pip install pyqt5
	pyuic5 -o rm102/mainwindow.py mainwindow.ui
	pyuic5 -o rm102/help_dialog.py help_dialog.ui
remove:
	rm102/mainwindow.py
install:
	python3 -m pip install .
uninstall:
	python3 -m pip uninstall registermachine102
