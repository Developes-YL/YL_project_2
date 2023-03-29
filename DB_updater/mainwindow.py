import sqlite3

from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5 import uic


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Support/mainUI.ui", self)
        self.load()
        self.titles = None

    def load(self):
        con = sqlite3.connect("MainDB2.db")
        cur = con.cursor()
        result = cur.execute("SELECT * FROM Students").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]) - 1)
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                if i == 0:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
                if j > 1:
                    self.tableWidget.setItem(i, j - 1, QTableWidgetItem(str(val)))
