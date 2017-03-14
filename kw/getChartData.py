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

        btn1 = QPushButton("getChartData", self)
        btn1.move(190, 10)
        btn1.clicked.connect(self.getChartData)

        # void OnEventConnect 통신 연결상태 변경시 이벤트
        self.kiwoom.OnEventConnect.connect(self.event_connect)
        self.kiwoom.OnReceiveTrData.connect(self.receive_trdata)

        # print("Calling getChartData()...")
        # self.getChartData("032860", 10)

    def event_connect(self, nErrCode):
        if nErrCode == 0:
            self.text_edit.append("로그인 성공")
            print("로그인 성공")
        elif nErrCode < 0:  # error
            self.text_edit.append("로그인 실패")
        self.text_edit.append(self.get_user_account)

    def getChartData(self, index="032860", interval=10):
        # InputValue 셋업
        print("Running getChartData", index, interval)
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드", index)
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "틱범위", str(interval))
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "수정주가구분", "1")

        ret = self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)",
                "opt10080_req", "opt10080", "0", "0101")
        print("CommRqData 실시: ", ret)

    def receive_trdata(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        if rqname == "opt10080_req":    # 주식 분봉 차트 조회 요청
            current = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)",
                    trcode, "", rqname, 0, "현재가")
            print(current)

    @property
    def get_user_account(self):
        """
        계좌번호 리턴.
        """
        ret = self.kiwoom.dynamicCall("GetLoginInfo(QString)",
            ["ACCNO"])
        # 마지막에 ;이 따라옴. 계좌번호 여러 개 있을 땐 마지막 것을 리턴.
        account_num = ret.split(';')[-2]

        return account_num

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
