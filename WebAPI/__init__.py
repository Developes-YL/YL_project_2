def new_path(name: str) -> str:
    path = __file__
    path = '/'.join(path.split('\\')[:-1])
    return path + "\\" + name


HOST = 'localhost'
PORT = 800
CODE_FILE = new_path("Support\\CODE.txt")
__all__ = ["HOST", "PORT", "CODE_FILE"]
