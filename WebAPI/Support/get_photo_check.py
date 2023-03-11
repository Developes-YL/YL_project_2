import requests

from WebAPI.Support.variables import HOST, PORT, CODE_FILE

with open(file=CODE_FILE, mode="r", encoding="utf-8") as f:
    current_code = f.readline()
res = requests.get(f"http://{HOST}:{PORT}/get_photo",
                   params={"code": current_code, "id": 0}).json()
if res["ok"]:
    print(res["photo"])
