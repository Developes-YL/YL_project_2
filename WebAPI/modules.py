import base64
import datetime
import sqlite3

from WebAPI import TIME_CHANGE, DB, CODE_FILE, PHOTOS_DIR


def get_inf(student_id: int, student_code: str) -> dict:
    ans = list()
    res = get_status(student_id, student_code)
    if res == "error":
        return "error"
    ans.append(res)
    res = load_inf_from_dp(student_id)
    if res == "error":
        return "error"
    ans.extend(res)
    image = get_photo_from_db(student_id)
    if image == "error":
        return "error"
    ans.append(image)
    return ans


def load_inf_from_dp(student_id: int):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    que = f'SELECT surname, name, patronymic, grade_number, grade_letter FROM Students WHERE tg_id = {student_id}'
    result = cur.execute(que).fetchone()
    if not result:
        return "error"
    result = list(map(str, result))
    name = ' '.join(result[:3])
    grade = ' '.join(result[3:])
    con.close()
    return [name, grade]


def get_status(student_id: int, code: str) -> bool:
    time_now = datetime.datetime.now().time()
    time_change = datetime.datetime.strptime(TIME_CHANGE, "%H:%M").time()
    if time_now > time_change:
        lunch_or_breafast = "lunch"
    else:
        lunch_or_breafast = "breakfast"
    con = sqlite3.connect(DB)
    cur = con.cursor()
    id_in_db = cur.execute("SELECT id FROM Students WHERE tg_id = ?", (student_id,)).fetchone()
    if not id_in_db or len(id_in_db) == 0:
        return "error"
    id_in_db = id_in_db[0]
    que = f'SELECT {lunch_or_breafast} FROM Codes WHERE id = {id_in_db}'
    result = cur.execute(que).fetchone()
    cur.execute(f"UPDATE Codes SET {lunch_or_breafast} = '0' WHERE id = {id_in_db}")
    if len(result) == 0:
        return "error"
    if result[0] == "0":
        return False
    con.commit()
    con.close()
    return result[0] == code


def check_code(code: str) -> bool:
    with open(file=CODE_FILE, mode="r", encoding="utf-8") as f:
        current_code = f.readline()
    return current_code == code


def get_photo_from_db(student_id: int):
    try:
        with open(PHOTOS_DIR + "/" + str(student_id) + ".png", "rb") as file:
            image = base64.b64encode(file.read()).decode("utf-8")
    except:
        try:
            with open(PHOTOS_DIR + "/" + str(student_id) + ".jpg", "rb") as file:
                image = base64.b64encode(file.read()).decode("utf-8")
        except:
            return "error"
    return image
