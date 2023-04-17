def new_path(name: str) -> str:
    path = __file__
    path = '/'.join(path.split('\\')[:-1])
    return path + "/" + name


HOST = 'localhost'
PORT = 800
CODE_FILE = new_path("Support/CODE.txt")
UI_FILE = new_path('Support/main_window.ui')
DB_PATH = new_path("../DB")
ACCEPT = new_path("Support/accept.png")
REJECT = new_path("Support/reject.png")
PHOTOS_DIR = DB_PATH + "/DATA"
DB = DB_PATH + "/MainDB.db"
