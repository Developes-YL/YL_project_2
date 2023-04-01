import sqlite3
import bot


def update_result():
    con = sqlite3.connect("../DB/MainDB.db")
    cur = con.cursor()
    ids = cur.execute("SELECT id FROM Rejected_requests").fetchall()
    for id0 in ids:
        print(id0)
        tg_id = cur.execute(f"SELECT tg_id FROM Students WHERE id = {id0[0]}").fetchone()
        print(tg_id[0])
        bot.bot.send_message(tg_id[0], "Ваша перевод некорректен")


update_result()