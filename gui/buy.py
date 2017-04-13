import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from kw import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.comm_connect()

    """
    # testing deposit
    kiwoom.set_input_value("계좌번호", "8089008711")
    kiwoom.set_input_value("비밀번호", "0000")
    kiwoom.comm_rq_data("opw00001_req", "opw00001", 0, "2000")
    time.sleep(3)
    print(kiwoom.d2_deposit)
    """

    kiwoom.set_input_value("계좌번호", "8089008711")
    kiwoom.comm_rq_data("opw00018_req", "opw00018", 0, "2000")