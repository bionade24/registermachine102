# -*- Makefile -*-

all:
	python3 -m pip install pyqt5
	pyuic5 -o rm102/mainwindow.py mainwindow.ui
remove:
	rm102/mainwindow.py
install:
	python3 -m pip install .
uninstall:
	python3 -m pip uninstall registermachine102
