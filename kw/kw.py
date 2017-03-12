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
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

        btn1 = QPushButton("Log In", self)
        btn1.move(20, 20)
        btn1.clicked.connect(self.btn_login)



    def btn_login(self):
        ret = self.kiwoom.dynamicCall("CommConnect()")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
