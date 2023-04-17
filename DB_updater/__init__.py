frame = None


def change_window(window):
    global frame
    frame = window()
    frame.show()


def new_path(name: str) -> str:
    path = __file__
    path = '/'.join(path.split('\\')[:-1])
    return path + "/" + name


DB_PATH = new_path("../DB")
DB = DB_PATH + "/MainDB.db"
