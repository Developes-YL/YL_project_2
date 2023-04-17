from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect, QCoreApplication, QMetaObject
from PyQt5.QtWidgets import *


class MainW(QMainWindow):
    def __init__(self):
        super().__init__()
        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)
        self.grid = QGridLayout(self.centralWidget)
        self.centralWidget.setLayout(self.grid)
        self.setupUi(self)

    def setupUi(self, main_window):
        self.menu = QPushButton()
        self.menu.setObjectName(u"menu")
        self.menu.setGeometry(QRect(10, 10, 111, 61))
        self.grid.addWidget(self.menu, 0, 0)
        self.verticalLayoutWidget = QWidget(self.centralWidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(280, 59, 1351, 911))
        self.grid.addWidget(self.verticalLayoutWidget, 1, 1)
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.tableWidget = QTableWidget(self.verticalLayoutWidget)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setProperty("showDropIndicator", False)
        self.tableWidget.setDragDropOverwriteMode(False)
        self.verticalLayout.addWidget(self.tableWidget)
        self.verticalLayoutWidget_2 = QWidget(self.centralWidget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(1680, 310, 160, 104))
        self.grid.addWidget(self.verticalLayoutWidget_2, 1, 2)
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QVBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.spinBox = QSpinBox(self.verticalLayoutWidget_2)
        self.spinBox.setObjectName(u"spinBox")
        self.horizontalLayout.addWidget(self.spinBox)
        self.pushButton_3 = QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.pushButton = QPushButton(self.centralWidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(30, 930, 133, 23))
        self.grid.addWidget(self.pushButton, 2, 2)
        self.retranslateUi(main_window)
        QMetaObject.connectSlotsByName(main_window)
        # setupUi

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(QCoreApplication.translate("main_window", u"main_window", None))
        self.menu.setText(QCoreApplication.translate("main_window", u"\u043c\u0435\u043d\u044e", None))
        self.pushButton_3.setText(QCoreApplication.translate("main_window",
                                                             u"\u041f\u0435\u0440\u0435\u043a\u043b\u044e\u0447\u0438"
                                                             u"\u0442\u044c",
                                                             None))
        self.pushButton.setText(QCoreApplication.translate("main_window",
                                                           u"\u041f\u043e\u0434\u0442\u0432\u0435\u0440\u0434\u0438"
                                                           u"\u0442\u044c "
                                                           u"\u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u044f",
                                                           None))
    # retranslateUi
