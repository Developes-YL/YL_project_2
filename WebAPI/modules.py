from WebAPI.Support.variables import CODE_FILE


def get_inf_from_db(student_id: int) -> dict:
    return {"id": student_id}


def get_status(for_lunch: bool, student_id: int, code: str) -> bool:
    return [for_lunch, student_id, code]


def check_code(code: str) -> bool:
    with open(file=CODE_FILE, mode="r", encoding="utf-8") as f:
        current_code = f.readline()
    return hash(current_code) == code
