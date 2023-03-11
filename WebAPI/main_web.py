import json
import imageio.v3 as iio
import numpy as np
from bottle import route, request, run
from PIL import Image

from WebAPI import HOST, PORT
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
def check() -> dict:
    if not hasattr(request.query, "code"):
        return {"ok": False, "description": "неверный код"}
    code = request.query.code
    return {"ok": check_code(code)}


@route('/photo')
def get_photo() -> dict:
    if not hasattr(request.query, "code"):
        return {"ok": False, "description": "неверный код"}
    if not hasattr(request.query, "id"):
        return {"ok": False, "description": "неверный id"}
    filename = "Support/bomb2.png"
    image = Image.open(filename)
    json_data = json.dumps(np.array(image).tolist())
    ans = {"ok": True, "f": json_data}
    return ans


def main():
    run(host=HOST, port=PORT)


if __name__ == "__main__":
    main()
