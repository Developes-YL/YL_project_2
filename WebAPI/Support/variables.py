import os.path


def new_path(name: str) -> str:
    print(os.path.abspath(name))
    return os.path.abspath(name)


HOST = 'localhost'
PORT = 800
CODE_FILE = new_path("Support/CODE.txt")
