import requests

from QR_code_reader import CODE_FILE, HOST, PORT


def get_inf_from_bot(code, student_id):
    with open(file=CODE_FILE, mode="r", encoding="utf-8") as f:
        current_code = f.readline()
    params = {"code": current_code,
              "id": student_id,
              "student_code": code}
    res = requests.get(f"http://{HOST}:{PORT}/get_information", params=params).json()
    return res
