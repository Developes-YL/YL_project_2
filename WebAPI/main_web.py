from bottle import route, request, run
from PyQt5.QtGui import QPixmap

from WebAPI.Support.variables import PORT, HOST
from WebAPI.modules import get_inf_from_db, check_code


@route('/get_inf')
def get_information() -> dict:
    if not hasattr(request.query, "code"):
        return {"ok": False, "description": "неверный код"}
    if not hasattr(request.query, "id"):
        return {"ok": False, "description": "неверный id"}
    student_id = request.query.id
    inf = get_inf_from_db(student_id)
    return inf


@route('/check')
def get_information() -> dict:
    if not hasattr(request.query, "code"):
        return {"ok": False, "description": "неверный код"}
    code = request.query.code
    return {"ok": check_code(code)}


@route('/photo')
def get_information() -> dict:
    if not hasattr(request.query, "code"):
        return {"ok": False, "description": "неверный код"}
    if not hasattr(request.query, "id"):
        return {"ok": False, "description": "неверный id"}
    ans = {"ok": True, "photo": QPixmap("Support/bombs.png")}
    return {"ok": True}


def main():
    run(host=HOST, port=PORT)


if __name__ == "__main__":
    main()
