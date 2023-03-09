from bottle import route, request, run

from WebAPI.Support.variables import PORT, HOST
from WebAPI.modules import get_inf_from_db


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
    return {"ok": True}


def main():
    run(host=HOST, port=PORT)


if __name__ == "__main__":
    main()
