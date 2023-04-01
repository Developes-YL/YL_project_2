# скрипт для проверки работы main файла
import sys

import requests

from WebAPI import HOST, PORT, CODE_FILE

with open(file=CODE_FILE, mode="r", encoding="utf-8") as f:
    current_code = f.readline()
try:
    res = requests.get(f"http://{HOST}:{PORT}/check_code",
                       params={"code": current_code}).json()
except:
    print("Error1")
    sys.exit()
if res["ok"]:
    print("Ok")
else:
    print("Error2", res["description"])
