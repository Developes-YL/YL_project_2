import sqlite3
from . import TIME_CHANGE, TIME_STOP, TIME_START


def get_name_from_db(tg_id: str) -> list:
    con = sqlite3.connect("../DB/MainDB.db")
    cur = con.cursor()
    que = f"SELECT name, surname from Students WHERE tg_id = {tg_id}"
    res = cur.execute(que).fetchone()
    con.close()
    if not res:
        return ["unnamed", "user"]
    if len(res) != 2:
        return ["unnamed", "user"]
    return res


def is_user_in_db(tg_id: int) -> bool:
    con = sqlite3.connect("../DB/MainDB.db")
    cur = con.cursor()
    que = f"SELECT tg_id from Students WHERE tg_id = {str(tg_id)}"
    res = cur.execute(que).fetchall()
    con.close()
    return len(res) != 0


def get_code(tg_id: str) -> str:
    time_now = datetime.datetime.now().time()
    time_change = datetime.datetime.strptime(TIME_CHANGE, "%H:%M").time()
    time_stop = datetime.datetime.strptime(TIME_STOP, "%H:%M").time()
    time_start = datetime.datetime.strptime(TIME_START, "%H:%M").time()
    if time_now < time_start:
        return "error"
    if time_now > time_stop:
        return "error"
    if time_now > time_change:
        for_lunch = True
    else:
        for_lunch = False

    conn = sqlite3.connect('../DB/MainDB.db')  # установление соединения с базой данных
    cur = conn.cursor()  # создание курсора
    st_id = cur.execute(f"SELECT id FROM Students WHERE tg_id = {tg_id}").fetchone()[0]
    cur.execute(f'SELECT {"lunch" if for_lunch else "breakfast"} FROM Codes WHERE id = {st_id}')
    code = cur.fetchone()  # получение результата
    conn.close()  # закрытие соединения с базой данных
    return code[0] if code else 'error'


def add_inf_to_db(inf: dict):
    con = sqlite3.connect("../DB/MainDB.db")
    cur = con.cursor()
    que = "INSERT INTO Students (tg_id, surname, name, patronymic, grade_number, grade_letter) " \
          f"VALUES ({inf['tg_id']}, '" + inf['surname'] + "', '" + inf['name'] + \
          "', '" + inf['patronymic'] + "', " + str(inf['grade_number']) + ", '" + inf['grade_letter'] + "')"
    cur.execute(que)
    con.commit()
    con.close()


def get_prices():
    with open("../DB/settings.txt", "r") as file:
        price_this_month_breakfast = float(file.readline().split('=')[1])
        price_this_month_lunch = float(file.readline().split('=')[1])
        price_next_month_breakfast = float(file.readline().split('=')[1])
        price_next_month_lunch = float(file.readline().split('=')[1])
    return [price_this_month_breakfast, price_this_month_lunch, price_next_month_breakfast, price_next_month_lunch]


def get_classes():
    with open("../DB/settings.txt", "r", encoding="utf-8") as file:
        for i in range(8):
            file.readline()
        class_numbers = file.readline().strip().split(':')[1].split(';')
        class_letters = file.readline().strip().split(':')[1].split(';')
    return [class_numbers, class_letters]
