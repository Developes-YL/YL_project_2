import json
import sys
import requests
from PIL import Image
from numpy import array

from WebAPI import HOST, PORT, CODE_FILE, PHOTOS_DIR

with open(file=CODE_FILE, mode="r", encoding="utf-8") as f:
    current_code = f.readline()
try:
    res = requests.get(f"http://{HOST}:{PORT}/get_photo",
                       params={"code": current_code, "id": "0"}).json()
except:
    print("Error1")
    sys.exit()

if res["ok"]:
    if "image" in res.keys():
        data_1 = res["image"]
        image = Image.open(PHOTOS_DIR + "/0.png")
        data_2 = json.dumps(array(image).tolist())
        if data_1 == data_2:
            print("ok")
        else:
            print("Error4")
    else:
        print("Error3")
else:
    print("Error2", res["description"])

