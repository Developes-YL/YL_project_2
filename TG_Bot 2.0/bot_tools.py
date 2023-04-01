import sqlite3
import bot


def update_result():
    con = sqlite3.connect("..DB/MainDB.db")
    cur = con.cursor()
    ids = cur.execute("SELECT id FROM Rejected_requests").fetchall()
    for id0 in ids:
        tg_id = cur.execute("SELECT tg_id FROM Students WHERE id = ?", (id0,))
        bot.bot.send_message(tg_id, "Ваша перевод некорректен")


update_result()