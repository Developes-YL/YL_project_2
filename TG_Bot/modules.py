import calendar
import datetime
import random
import sched
import sqlite3
import string
import threading
import time


def setup_time_func():
    timer1 = threading.Thread(target=a)
    timer1.start()
    timer2 = threading.Thread(target=b)
    timer2.start()
    print("таймеры запущены")


def a():
    now = datetime.datetime.now()
    time_start = (calendar.monthrange(now.year, now.month)[1] - now.today().day) * 24 * 3600 + \
                 ((24 - now.time().hour) * 60 - now.time().minute) * 60 - now.time().second + 60
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(time_start, 1, change_month)
    scheduler.run()


def b():
    now = datetime.datetime.now()
    with open('../DB/settings.txt', 'r') as file:
        for i in range(7):
            file.readline()
        line = file.readline().split("=")[1].rstrip()
    time2 = datetime.datetime.strptime(line, "%H:%M").time()
    t = datetime.datetime.combine(now.date(), time2)
    dif = 24*3600 - (now - t).total_seconds()
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(dif, 1, change_month)
    scheduler.run()


def change_month():
    con = sqlite3.connect("../DB/MainDB.db")
    cur = con.cursor()
    cur.execute("DELETE FROM Lunch_this")
    lunches = cur.execute("SELECT * FROM lunch_next").fetchall()
    for i in range(len(lunches)):
        lunches[i] = tuple(map(str, lunches[i]))
    for row in lunches:
        cur.execute(f"INSERT INTO lunch_this VALUES {row}")
    cur.execute("DELETE FROM Lunch_next")

    cur.execute("DELETE FROM Breakfast_this")
    breakfasts = cur.execute("SELECT * FROM breakfast_next").fetchall()
    for i in range(len(breakfasts)):
        breakfasts[i] = tuple(map(str, breakfasts[i]))
    for row in breakfasts:
        cur.execute(f"INSERT INTO breakfast_this VALUES {row}")
    cur.execute("DELETE FROM Breakfast_next")
    cur.execute("DELETE FROM Request")
    con.commit()
    con.close()
    a()


def change_day():
    today = datetime.datetime.now().today().day
    con = sqlite3.connect("../DB/MainDB.db")
    cur = con.cursor()
    cur.execute("DELETE FROM Codes")
    lunches = cur.execute(f"SELECT id FROM Lunch_this WHERE _{today} = '+'").fetchall()
    breakfasts = cur.execute(f"SELECT id FROM Breakfast_this WHERE _{today} = '+'").fetchall()
    for i in set(lunches + breakfasts):
        lunch = "0"
        breakfast = "0"
        if i in lunches:
            lunch = generate_code()
        if i in breakfasts:
            breakfast = generate_code()
        cur.execute(f"INSERT INTO Codes VALUES ({i[0]}, '{lunch}', '{breakfast}')")
    con.commit()
    con.close()
    b()


def generate_code() -> str:
    chars = string.ascii_letters + string.digits
    code = ''.join(random.choice(chars) for _ in range(30))
    return code
