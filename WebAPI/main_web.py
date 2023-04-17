from json import dumps
from numpy import array
from bottle import route, request, run

from WebAPI import HOST, PORT
from WebAPI.modules import get_inf, check_code, get_photo_from_db


@route('/get_information')
def get_information() -> dict:
    if not hasattr(request.query, "code"):
        return {"ok": False, "description": "неверный код"}
    code = request.query.code
    if not check_code(code):
        return {"ok": False, "description": "неверный код"}

    if not hasattr(request.query, "id"):
        return {"ok": False, "description": "неверный id"}
    student_id = request.query.id

    if not hasattr(request.query, "student_code"):
        return {"ok": False, "description": "неверный id"}
    student_code = request.query.student_code
    res = get_inf(student_id, student_code)
    print(res)
    if res and res != "error":
        status, name, grade, photo = res
        return {"ok": True, "status": status, "name": name, "grade": grade, "image": photo}
    return {"ok": False, "description": "ошибка во время получения информации из БД"}


@route('/check_code')
def check() -> dict:
    if not hasattr(request.query, "code"):
        return {"ok": False, "description": "неверный код"}
    code = request.query.code
    if check_code(code):
        return {"ok": True}
    return {"ok": False, "description": "неверный код"}


@route('/get_photo')
def get_photo() -> dict:
    if not hasattr(request.query, "code"):
        return {"ok": False, "description": "неверный код"}
    code = request.query.code
    if not check_code(code):
        return {"ok": False, "description": "неверный код"}

    if not hasattr(request.query, "id"):
        return {"ok": False, "description": "неверный id"}
    student_id = request.query.id
    image = get_photo_from_db(student_id)
    image_data = dumps(array(image).tolist())
    ans = {"ok": True, "image": image_data}
    return ans


def main():
    run(host=HOST, port=PORT)


if __name__ == "__main__":
    main()
