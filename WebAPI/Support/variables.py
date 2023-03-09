import os.path


def new_path(name: str) -> str:
    return os.path.abspath(name)


HOST = '192.168.0.101'
PORT = 800
CODE_FILE = new_path("CODE.txt")
