import json

import numpy as np
import requests
from PIL import Image

from WebAPI.Support import HOST, PORT, CODE_FILE

with open(file=CODE_FILE, mode="r", encoding="utf-8") as f:
    current_code = f.readline()
res = requests.get(f"http://{HOST}:{PORT}/photo",
                   params={"code": current_code, "id": "0"}).json()
if res["ok"]:
    if "f" in res.keys():
        img = res["f"]
        new_image = Image.fromarray(np.array(json.loads(img), dtype='uint8'))
        new_image.show()

