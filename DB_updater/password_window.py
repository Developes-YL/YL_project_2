import sqlite3

from PyQt5.QtWidgets import QDialog
from PyQt5 import uic

from DB_updater import change_window, DB
from main_window import MyWindow


class MyWindow2(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("Support/loginUI.ui", self)
        self.pushButton.clicked.connect(self.check)

    def check(self):
        login = self.login.text()
        password = self.password.text()
        self.password.setText("")
        con = sqlite3.connect(DB)
        cur = con.cursor()
        res = cur.execute(f"SELECT password FROM Admins WHERE login = '{login}'").fetchone()
        con.close()
        if len(res) > 0 and str(res[0]) == password:
            change_window(MyWindow)
