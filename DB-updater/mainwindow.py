import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic, QtGui
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("mainUI.ui", self)


