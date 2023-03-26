import sqlite3


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


def add_inf_to_db(inf: dict):
    con = sqlite3.connect("../DB/MainDB.db")
    cur = con.cursor()
    que = "INSERT INTO Students (tg_id, surname, name, patronymic, grade_number, grade_letter) " \
          f"VALUES ({inf['tg_id']}, '" + inf['surname'] + "', '" + inf['name'] + \
          "', '" + inf['patronymic'] + "', " + str(inf['grade_number']) + ", '" + inf['grade_letter'] + "')"
    cur.execute(que)
    con.commit()
    con.close()
