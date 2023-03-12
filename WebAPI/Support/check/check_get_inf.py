import json
import sys

import numpy as np
import requests
from PIL import Image

from WebAPI import HOST, PORT, CODE_FILE, PHOTOS_DIR

with open(file=CODE_FILE, mode="r", encoding="utf-8") as f:
    current_code = f.readline()
try:
    res = requests.get(f"http://{HOST}:{PORT}/get_information",
                       params={"code": current_code, "id": "0", "student_code": "2"}).json()
except:
    print("Error1")
    sys.exit()

if res["ok"]:
    print(res["status"], res["name"], res["grade"])
    Image.fromarray(np.array(json.loads(res["image"]), dtype='uint8')).show()
else:
    print("Error2", res["description"])

