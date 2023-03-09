import os.path


def new_path(name: str) -> str:
    return os.path.abspath(name)


FILE = 'TOKEN.txt'
