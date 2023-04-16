import sqlite3
import datetime


def check_time_in_interval(start_time_str, end_time_str):
    current_time = datetime.datetime.now().time()

    # преобразуем строки с начальным и конечным временем в объекты time
    start_time = datetime.datetime.strptime(start_time_str, '%H:%M').time()
    end_time = datetime.datetime.strptime(end_time_str, '%H:%M').time()

    if start_time <= current_time <= end_time:
        return True
    else:
        return False


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
    for_lunch = True
    conn = sqlite3.connect('../DB/MainDB.db')  # установление соединения с базой данных
    cur = conn.cursor()  # создание курсора
    st_id = cur.execute(f"SELECT id FROM Students WHERE tg_id = {tg_id}").fetchone()[0]
    cur.execute(f'SELECT {"lunch" if for_lunch else "breakfast"} FROM Codes WHERE id = {st_id}')
    code = cur.fetchone()  # получение результата
    conn.close()  # закрытие соединения с базой данных
    return code[0] if code[0] != '0' else 'error'


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


def add_days_to_db(days: dict, tg_id: int, number: str, sum: int):
    con = sqlite3.connect("../DB/MainDB.db")
    cur = con.cursor()
    id = cur.execute("SELECT id FROM Students WHERE tg_id = ?", (tg_id,)).fetchone()[0]
    days_in_month = dict()
    with open("../DB/days_next.txt") as file:
        for day in ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]:
            d = file.readline().strip().split(':')[1].split(';')
            d.remove('')
            days_in_month[day] = d
    lunch = []
    breakfast = []
    for day in days_in_month.keys():
        if day in days["lunch"]:
            for elem in days_in_month[day]:
                lunch.append(int(elem))
        if day in days["breakfast"]:
            for elem in days_in_month[day]:
                breakfast.append(int(elem))
    indexes = cur.execute("SELECT id FROM Request").fetchall()
    if (id,) in indexes:
        cur.execute(f"DELETE FROM Request WHERE id = {id}")
    lunch = ';'.join(map(str, lunch))
    breakfast = ';'.join(map(str, breakfast))
    cur.execute(f"INSERT INTO Request VALUES {(id, sum, number, lunch, breakfast)}")
    con.commit()
    con.close()
