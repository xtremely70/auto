import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from kw import *

form_class = uic.loadUiType("gui.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self._set_signal_slots()

        self.kiwoom = Kiwoom()
        self.kiwoom.comm_connect()

        self._set_account_info()

    def _set_signal_slots(self):
        """
        init 시점에 이벤트 슬롯 지정
        :return: n/a
        """
        self.lineEdit.textChanged.connect(self.code_changed)
        self.pushButton.clicked.connect(self.send_order)

    def _set_account_info(self):
        """
        계좌정보 
        :return: 
        """
        accounts_num = int(self.kiwoom.get_login_info("ACCOUNT_CNT"))
        accounts = self.kiwoom.get_login_info("ACCNO")
        accounts_list = accounts.split(';')[0:accounts_num]
        self.comboBox.addItems(accounts_list)

    def code_changed(self):
        """
        종목코드(lineEdit) 변동시 종목명 받아옴
        :return: 
        """
        code = self.lineEdit.text()
        name = self.kiwoom.get_master_code_name(code)
        self.lineEdit_2.setText(name)

    def send_order(self):
        order_type_lookup = {'신규매수': 1, '신규매도': 2, '매수취소': 3, '매도취소': 4}
        hoga_lookup = {'지정가': "00", '시장가': "03"}

        account = self.comboBox.currentText()
        order_type = self.comboBox_2.currentText()
        code = self.lineEdit.text()
        hoga = self.comboBox_3.currentText()
        num = self.spinBox.value()
        price = self.spinBox_2.value()
        self.kiwoom.send_order("send_order_req", "0101", account, order_type_lookup[order_type],
                               code, num, price, hoga_lookup[hoga], "")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
