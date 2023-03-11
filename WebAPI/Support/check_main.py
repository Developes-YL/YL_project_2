# скрипт для проверки работы main файла
import requests

from WebAPI.Support import HOST, PORT, CODE_FILE

with open(file=CODE_FILE, mode="r", encoding="utf-8") as f:
    current_code = f.readline()
res = requests.get(f"http://{HOST}:{PORT}/check",
                   params={"code": current_code}).json()
try:
    if res["ok"]:
        print("Ok")
    else:
        print("Error", res["description"])
except:
    print("Error")
