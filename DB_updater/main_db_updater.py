import sys
from PyQt5.QtWidgets import QApplication

from DB_updater import change_window
from password_window import MyWindow2


app = QApplication(sys.argv)
change_window(MyWindow2)
sys.exit(app.exec())
