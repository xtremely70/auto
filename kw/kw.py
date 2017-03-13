#-*-coding: utf-8 -*-
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyStock")
        self.setGeometry(300, 300, 300, 150)

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.dynamicCall("CommConnect()")

        # setting up text edit widget
        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10, 60, 280, 80)
        self.text_edit.setEnabled(False)

        self.kiwoom.OnEventConnect.connect(self.event_connect)

    def event_connect(self, nErrCode):
        if nErrCode == 0:
            self.text_edit.append("로그인 성공")
        elif nErrCode < 0:  # error
            self.text_edit.append("로그인 실패")

"""
        btn1 = QPushButton("Log In", self)
        btn1.move(20, 20)
        btn1.clicked.connect(self.btn_login)

        btn2 = QPushButton("Check status", self)
        btn2.move(20, 70)
        btn2.clicked.connect(self.btn2_clicked)

    def btn_login(self):
        ret = self.kiwoom.dynamicCall("CommConnect()")

    def btn2_clicked(self):
        if self.kiwoom.dynamicCall("GetConnectState()") == 1:
            self.statusBar().showMessage("Connected")
        else:
            self.statusBar().showMessage("Not connected")
"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
