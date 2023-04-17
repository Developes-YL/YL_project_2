def new_path(name: str) -> str:
    path = __file__
    path = '/'.join(path.split('\\')[:-1])
    return path + "/" + name


def read_settings_file() -> list:
    with open(SETTINGS, mode="r", encoding="utf-8") as f:
        lines = f.readlines()[:7]
        lines = list(map(lambda x: x.rstrip("\n").split('=')[1], lines))
        prices = list(map(int, lines[:4]))
        time = lines[4:]
        return prices + time


HOST = 'localhost'
PORT = 800
CODE_FILE = new_path("Support/CODE.txt")
DB_PATH = new_path("../DB")
PHOTOS_DIR = DB_PATH + "/DATA"
DB = DB_PATH + "/MainDB.db"
SETTINGS = DB_PATH + "/settings.txt"
*PRICES, TIME_START, TIME_CHANGE, TIME_STOP = read_settings_file()
