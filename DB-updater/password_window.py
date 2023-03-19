from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from mainwindow import MyWindow

class MyWindow2(QDialog):
    def __init__(self):
        self.newlogin = ''
        self.newpassword = ''
        self.login = 'admin'
        self.password = 'password'
        super().__init__()
        uic.loadUi("loginUI.ui", self)
        self.pushButton.clicked.connect(self.loginch)
        self.checked = 0

    def loginch(self):
        self.newlogin = self.textEdit.toPlainText()
        self.newpassword = self.textEdit_2.toPlainText()
        if self.newlogin == self.login and self.newpassword == self.password:
            global frame2
            frame2 = MyWindow()
            frame2.show()