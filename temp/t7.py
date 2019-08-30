import sys
from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import (QWidget, QLCDNumber, QSlider, QFormLayout, QGroupBox, QHBoxLayout,
    QVBoxLayout, QApplication, QMainWindow, QTabWidget, QLineEdit, QPushButton)
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QRegExp


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        tab1 = self.tab1_layout()
        tab2 = self.tab2_layout()
        tab3 = self.tab3_layout() 

        tabs = QTabWidget()
        tabs.addTab(tab1, '1st')
        tabs.addTab(tab2, '2nd')
        tabs.addTab(tab3, '3rd')
        tabs.addTab(tab4, '4th')

        
        


        

    def tab1_layout(self):
        self.le_ctaid = QLineEdit()
        self.le_bsid = QLineEdit()
        self.le_delay = QLineEdit()
        self.btn_login = QPushButton("로그인")

        flo1 = QFormLayout()
        flo1.addRow("세무사관리번호", self.le_ctaid)
        flo1.addRow("부서아이디", self.le_bsid)
        flo1.addRow("딜레이타임", self.le_delay)
        flo1.addRow(self.btn_login)

        gbox1 = QGroupBox("HomeTax Login")
        gbox2 = QGroupBox("GroupBox2")

        gbox1.setLayout(flo1)

        hbox = QHBoxLayout()
        hbox.addWidget(gbox1)
        hbox.addWidget(gbox2)

        return hbox
        
        
    def tab2_layout(self):
        pass
    def tab3_layout(self):
        pass


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())