import os, sys, time, json, zipfile

import PyQt5
# from PyQt5.Qt import QApplication
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QWidget, QDialog, QPushButton, QRadioButton, QLabel, QLineEdit, QAction, QToolTip,qApp 
from PyQt5.QtWidgets import QMessageBox, QTabWidget, QGridLayout, QGroupBox, QHBoxLayout, QVBoxLayout, QFormLayout
from PyQt5.QtGui import QIcon, QRegExpValidator, QDoubleValidator, QIntValidator, QFont
from PyQt5.QtCore import pyqtSlot, Qt, QRegExp

# class Ui_setting(QWidget):
class Ui_setting(QDialog):
    def __init__(self, parent=None):
        super().__init__()        
        self.setWindowTitle("기본사항 저장(변경)")

        # self.setGeometry(300,300,500,10)
        # 우하단 위젯
        rect = QDesktopWidget().availableGeometry()   # 작업표시줄 제외한 화면크기 반환
        max_x = rect.width()
        max_y = rect.height()

        width, height = 500 , 155
        left = max_x - width 
        top = max_y - height 

        self.setGeometry(left, top-250, width, height)

        self.initUI()
    
    def initUI(self):

        lb1 = QLabel("세무사관리번호")        
        lb2 = QLabel("부서아이디")
        lb3 = QLabel("홈택스대표아이디")        
        lb4 = QLabel("공인인증서명칭")                  
            
        le1 = QLineEdit()
        le2 = QLineEdit()
        le3 = QLineEdit()
        le4 = QLineEdit()

        lb11 = QLabel("비밀번호")   # 세무사관리번호     
        lb21 = QLabel("비밀번호")   # 부서아이디 
        lb31 = QLabel("딜레이타임") 
        lb41 = QLabel("비밀번호")   # 공인인증서명칭 
               

        le11 = QLineEdit()
        le21 = QLineEdit()
        le31 = QLineEdit()
        le41 = QLineEdit()

        btn1 = QPushButton("변경사항 저장")
        btn2 = QPushButton("인증서선택")
        btn3 = QPushButton("인증서정보저장")

        QToolTip.setFont(QFont('SansSerif', 10))
        lb11.setToolTip(' <b>세무사관리번호</b> 비밀번호...')
        lb21.setToolTip(' <b>부서아이디</b> 비밀번호...')
        lb41.setToolTip(' <b>공인인증서</b> 비밀번호...')
        le11.setToolTip(' <b>세무사관리번호</b> 비밀번호...')
        le21.setToolTip(' <b>부서아이디</b> 비밀번호...')
        le41.setToolTip(' <b>공인인증서</b> 비밀번호...')
        btn3.setToolTip(' <b>공인인증서</b>명칭 비밀번호 저장...')

        le31.setStyleSheet(
                """QLineEdit { background-color: #f0f0f0; color: blue; font: bold }""")
        le4.setStyleSheet(
                """QLineEdit { background-color: #f0f0f0; color: blue }""")
        le41.setStyleSheet(
                """QLineEdit { background-color: #f0f0f0; color: blue }""")
        btn1.setStyleSheet(
                """QPushButton { color: blue; font: bold }""")
      
        grid = QGridLayout()
        
        grid.addWidget(lb1 , 0, 0)
        grid.addWidget(le1 , 0, 1)
        grid.addWidget(lb11, 0, 2)
        grid.addWidget(le11, 0, 3)

        grid.addWidget(lb2 , 1, 0)
        grid.addWidget(le2 , 1, 1)
        grid.addWidget(lb21, 1, 2)
        grid.addWidget(le21, 1, 3)

        grid.addWidget(lb3 , 2, 0)
        grid.addWidget(le3 , 2, 1)
        grid.addWidget(lb31, 2, 2)
        grid.addWidget(le31, 2, 3)

        grid.addWidget(lb4 , 3, 0)
        grid.addWidget(le4 , 3, 1)
        grid.addWidget(lb41, 3, 2)
        grid.addWidget(le41, 3, 3)
        
        grid.addWidget(btn1 , 4, 1)
        grid.addWidget(btn2, 4, 2)
        grid.addWidget(btn3, 4, 3)
     
        self.setLayout(grid)

        self.show()

    

if __name__ == "__main__":

    app = QApplication(sys.argv)
    ex = Ui_setting()
    sys.exit(app.exec_())
