import sqlite3

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
        login = self.login.text()
        password = self.password.text()
        self.password.setText("")
        con = sqlite3.connect("../DB/MainDB.db")
        cur = con.cursor()
        res = cur.execute(f"SELECT password FROM Admins WHERE login = '{login}'").fetchall()
        con.close()
        if len(res) > 0 and str(res[0][0]) == password:
            change_window(MyWindow)
