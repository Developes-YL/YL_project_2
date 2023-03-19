import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5 import uic
from password_window import MyWindow2


app = QApplication(sys.argv)
frame = MyWindow2()
frame.show()



sys.exit(app.exec())
