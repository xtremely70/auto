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
        btn1.clicked.connect(self.get_chart_data)

        btn2 = QPushButton("sendOrder", self)
        btn2.move(50, 10)
        btn2.clicked.connect(self.send_order)

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

    def get_chart_data(self):
        # InputValue 셋업
        print("Running getChartData")
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드", "032860")
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "틱범위", "10")
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "수정주가구분", "1")

        ret = self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)",
                ["opt10080_req", "opt10080", "0", "0101"])
        print("CommRqData 실시: ", ret)

    def send_order(self):
        """
        self.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                         [rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no])
        """
        ret = self.kiwoom.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                         ["rq0000", "1000", "8089008711", 1, "032860", 1, 0, "03", ""])
        print("send_order 실행", ret)


    def receive_trdata(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        print("TR data received.", rqname)
        if rqname == "opt10080_req":    # 주식 분봉 차트 조회 요청
            for i in range(0, 100):
                current_time = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)",
                        [trcode, "", rqname, i, "체결시간"])
                current = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)",
                        [trcode, "", rqname, i, "현재가"])
                print(current_time, current)

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
