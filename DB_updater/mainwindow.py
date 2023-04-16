import sqlite3

from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView

from Support.mainW import MainW


class MyWindow(MainW):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(250, 150)
        self.resize(900, 600)
        self.load()
        self.rejected = []
        self.pushButton_3.clicked.connect(self.reject)
        self.pushButton.clicked.connect(self.accept)

    def load(self):
        con = sqlite3.connect("../DB/MainDB.db")
        cur = con.cursor()
        que = """SELECT Students.id, Students.surname, Students.name, 
                Students.patronymic, Students.grade_number, Students.grade_letter, Request.codes, 
                Request.sum FROM Students JOIN Request ON Students.id = Request.id"""
        self.res = cur.execute(que).fetchall()
        self.res = list(map(lambda x: [*x, self.res.index(x)], self.res))
        con.close()
        visible_inf = []
        for i, elem in enumerate(self.res):
            visible_inf.append([elem[-1], ' '.join(elem[1:4]), f'{elem[4]} "{elem[5].upper()}"', elem[6], elem[7]])
        self.updateTable(visible_inf)

    def updateTable(self, inf):
        self.tableWidget.setRowCount(len(inf))
        self.tableWidget.setColumnCount(5)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.titles = ["N", "ФИО", "Класс", "Номер перевода", "Сумма"]
        for i, row in enumerate(inf):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))

    def reject(self):
        index = self.spinBox.value()
        n = list(map(lambda x: x[-1], self.res)).index(index)
        if self.res[n] not in self.rejected:
            self.rejected.append(self.res[n])
        lst = []
        for i, elem in enumerate(self.res):
            if i in map(lambda x: x[-1], [*self.rejected]):
                continue
            lst.append([elem[-1], ' '.join(elem[1:4]), f'{elem[4]} "{elem[5].upper()}"', elem[6], elem[7], i])
        self.updateTable(lst)

    def accept(self):
        con = sqlite3.connect("../DB/MainDB.db")
        cur = con.cursor()
        que = """DELETE FROM Request WHERE id = ?"""
        indexes_l = list(map(lambda x: x[0], cur.execute("SELECT id FROM lunch_next").fetchall()))
        indexes_b = list(map(lambda x: x[0], cur.execute("SELECT id FROM breakfast_next").fetchall()))
        for elem in self.res:
            if elem[0] in map(lambda x: x[0], self.rejected):
                pass
                # отправка сообщения
            else:
                days_l, days_b = cur.execute("SELECT days_l, days_b "
                                             "FROM Request WHERE id = ?", (elem[0],)).fetchall()[0]
                days_l = days_l.split(';')
                days_b = days_b.split(';')
                days = range(1, 32)
                lst = []
                for n, day in enumerate(days):
                    lst.append([])
                    if str(day) in days_b:
                        lst[n].append("+")
                    else:
                        lst[n].append("-")
                    if str(day) in days_l:
                        lst[n].append("+")
                    else:
                        lst[n].append("-")
                lunches = [elem[0]] + list(map(lambda x: x[0], lst))
                breakfasts = [elem[0]] + list(map(lambda x: x[1], lst))
                q = "INSERT INTO lunch_next VALUES (" + str(lunches)[1:-1] + ")"
                if elem[0] not in indexes_l:
                    cur.execute(q)
                q = "INSERT INTO breakfast_next VALUES (" + str(breakfasts)[1:-1] + ")"
                if elem[0] not in indexes_b:
                    cur.execute(q)
            cur.execute(que, (elem[0], )).fetchall()

        self.rejected = []
        self.res = []
        con.commit()
        con.close()
        self.load()
