import sys
from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import (QWidget, QLCDNumber, QSlider, QFormLayout, QGroupBox, QHBoxLayout,
    QVBoxLayout, QApplication, QMainWindow, QTabWidget, QLineEdit, QPushButton)
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QRegExp


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget() 

        tab1.setLayout(self.tab1_layout())
        tab2.setLayout(self.tab2_layout())
        tab3.setLayout(self.tab3_layout())
        # tab2 = self.tab2_layout()
        # tab3 = self.tab3_layout() 

        tabs = QTabWidget()
        # tabs.setLayout(tab1)
        tabs.addTab(tab1, "HomeTax")
        tabs.addTab(tab2, "2nd Tab")
        tabs.addTab(tab3, "3rd Tab")

        self.setCentralWidget(tabs)

        self.show()
        

    def tab1_layout(self):
        self.le_ctaid = QLineEdit()
        self.le_bsid = QLineEdit()
        self.le_delay = QLineEdit()
        self.btn_login = QPushButton("login")
        self.btn_save = QPushButton("save")

        hbox_s = QHBoxLayout()
        hbox_s.addWidget(self.btn_login)
        hbox_s.addWidget(self.btn_save)

        flo1 = QFormLayout()
        flo1.addRow("세무사관리번호", self.le_ctaid)
        flo1.addRow("부서아이디", self.le_bsid)
        flo1.addRow("딜레이타임", self.le_delay)
        flo1.addRow(hbox_s)

        gbox1 = QGroupBox("HomeTax Login")
        gbox2 = QGroupBox("GroupBox2")

        gbox1.setLayout(flo1)

        hbox = QHBoxLayout()
        hbox.addWidget(gbox1)
        hbox.addWidget(gbox2)

        return hbox
        
        
    def tab2_layout(self):
        btn = QPushButton('comming soon...')
        hbox = QHBoxLayout()
        hbox.addWidget(btn)
        return hbox

    def tab3_layout(self):
        btn = QPushButton('comming soon...')
        hbox = QHBoxLayout()
        hbox.addWidget(btn)
        return hbox


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())