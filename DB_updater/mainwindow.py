import sqlite3

from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5 import uic


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Support/mainUI.ui", self)
        self.load()
        self.titles = None
        self.pushButton_3.clicked.connect(self.deldur)

    def load(self):
        con = sqlite3.connect("MainDB2.db")
        cur = con.cursor()
        result = cur.execute("SELECT * FROM Students").fetchall()
        result2 = cur.execute("SELECT * FROM Request").fetchall()
        result3 = []
        for i in range(len(result)):
            result3.append((result[0][0], result[0][2], result[0][3], result[0][4], result[0][5], result2[0][1], result2[0][3], result2[0][4], result[0][6]))
        print(result3)
        self.tableWidget.setRowCount(len(result3))
        self.tableWidget.setColumnCount(len(result3[0]))
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result3):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def deldur(self):
        a = self.spinBox.value()
        con = sqlite3.connect("MainDB2.db")
        cur = con.cursor()
        result = cur.execute("SELECT * FROM Students").fetchall()
        if result[a - 1][6] == 'true':
            cur.execute(f"""UPDATE Students SET dyrachyo = 'false' WHERE id = {a}""")
        else:
            cur.execute(f"""UPDATE Students SET dyrachyo = 'true' WHERE id = {a}""")
        self.load()