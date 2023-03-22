from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Support/mainUI.ui", self)


