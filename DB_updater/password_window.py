from PyQt5.QtWidgets import QDialog
from PyQt5 import uic

from DB_updater import change_window
from mainwindow import MyWindow


class MyWindow2(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("Support/loginUI.ui", self)
        self.pushButton.clicked.connect(self.check)
        self.checked = 0

    def check(self):
        login = self.textEdit.toPlainText()
        password = self.textEdit_2.toPlainText()
        self.textEdit_2.setText("")
        with open("Support/passwords.txt", "r") as f:
            passwords = dict()
            lines = f.readlines()
            for line in lines[1:]:
                passwords[line.split(';')[0]] = line.split(';')[1].rstrip('\n')

        if login in passwords.keys() and password == passwords[login]:
            change_window(MyWindow)
