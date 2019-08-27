import os, sys, time, json, zipfile, subprocess

import PyQt5
# from PyQt5.Qt import QApplication
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDesktopWidget, QWidget, QDialog, 
                            QPushButton, QRadioButton, QLabel, QLineEdit, QAction, QToolTip, qApp)
from PyQt5.QtWidgets import QMessageBox, QTabWidget, QGridLayout, QGroupBox, QHBoxLayout, QVBoxLayout, QFormLayout
from PyQt5.QtGui import QIcon, QRegExpValidator, QDoubleValidator, QIntValidator, QFont
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QRegExp

# 상위폴더 내 파일 import  https://brownbears.tistory.com/296
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from data import setdata, data
from sites import hometax, naver
from utils import Util, driverutil

# 변수의 스코프  https://umbum.tistory.com/823
nts_dict = hometax.nts_dict

# class Ui_setting(QDialog):
#     def __init__(self, parent=None):
#         super().__init__()
         
#         self.cta_id = nts_dict['secret']['세무사관리번호']
#         self.bs_id = nts_dict['secret']['부서아이디']
#         self.super_id = nts_dict['secret']['수퍼아이디'] 
#         self.cert_name = nts_dict['secret']['공인인증서명칭']
#         self.cta_pw = nts_dict['secret']['세무사비번']
#         self.bs_pw = nts_dict['secret']['부서비번'] 
#         self.delay_time = str(nts_dict['secret']['딜레이타임']) 
#         self.cert_pw = nts_dict['secret']['공인인증서비번'] 

#         self.setWindowTitle("기본사항 저장(변경)")

#         # 우하단 위젯   # self.setGeometry(300,300,500,10)
#         rect = QDesktopWidget().availableGeometry()   # 작업표시줄 제외한 화면크기 반환
#         max_x = rect.width()
#         max_y = rect.height()

#         width, height = 500 , 155
#         left = max_x - width 
#         top = max_y - height 

#         self.setGeometry(left, top-250, width, height)

#         # 인포텍 모쥴 설치 
#         # driverutil.setup_iftCertAdapter()
        
#         self.initUI()
    
#     def initUI(self):

#         lb1 = QLabel("세무사관리번호")        
#         lb2 = QLabel("부서아이디")
#         lb3 = QLabel("홈택스대표아이디")        
#         lb4 = QLabel("공인인증서명칭") 

#         lb11 = QLabel("비밀번호")   # 세무사관리번호     
#         lb21 = QLabel("비밀번호")   # 부서아이디 
#         lb31 = QLabel("딜레이타임") 
#         lb41 = QLabel("비밀번호")   # 공인인증서명칭                  
            
#         self.le1 = QLineEdit()
#         self.le2 = QLineEdit()
#         self.le3 = QLineEdit()
#         self.le4 = QLineEdit()

#         self.le11 = QLineEdit()
#         self.le21 = QLineEdit()
#         self.le31 = QLineEdit()
#         self.le41 = QLineEdit()

#         btn1 = QPushButton("변경사항 저장")
#         btn2 = QPushButton("인증서선택")
#         btn3 = QPushButton("인증서정보저장")

#         QToolTip.setFont(QFont('SansSerif', 10))
#         lb11.setToolTip(' <b>세무사관리번호</b> <br>비밀번호...')
#         lb21.setToolTip(' <b>부서아이디</b> 비밀번호...')
#         lb41.setToolTip(' <b>공인인증서</b> 비밀번호...')
#         self.le11.setToolTip(' <b>세무사관리번호</b> 비밀번호...')
#         self.le21.setToolTip(' <b>부서아이디</b> 비밀번호...')
#         self.le41.setToolTip(' <b>공인인증서</b> 비밀번호...')
#         btn3.setToolTip(' <b>공인인증서</b>명칭 비밀번호 저장...')

#         self.le31.setStyleSheet(
#                 """QLineEdit { background-color: #f0f0f0; color: blue; font: bold }""")
#         self.le4.setStyleSheet(
#                 """QLineEdit { background-color: #f0f0f0; color: blue }""")
#         self.le41.setStyleSheet(
#                 """QLineEdit { background-color: #f0f0f0; color: blue }""")
#         btn1.setStyleSheet(
#                 """QPushButton { color: blue; font: bold }""")

#         self.le1.setPlaceholderText(nts_dict['secret']['세무사관리번호'])
#         self.le2.setPlaceholderText(nts_dict['secret']['부서아이디'])
#         self.le3.setPlaceholderText(nts_dict['secret']['수퍼아이디'])
#         self.le4.setPlaceholderText(nts_dict['secret']['공인인증서명칭'])

#         self.le11.setPlaceholderText(nts_dict['secret']['세무사비번'])
#         self.le21.setPlaceholderText(nts_dict['secret']['부서비번'])
#         self.le31.setPlaceholderText(str(nts_dict['secret']['딜레이타임']))
#         self.le41.setPlaceholderText(nts_dict['secret']['공인인증서비번'])
#         # 입력제한 http://bitly.kr/wmonM2
#         reg_ex = QRegExp("[0-9]+.?[0-9]{,2}")
#         input_validator = QRegExpValidator(reg_ex, self.le31)
#         # double_validator = QDoubleValidator(-999.0, 999.0, 2)   ### http://bitly.kr/wmonM2
#         self.le31.setValidator(input_validator)      # double_validator)  
#         self.le31.setMaxLength(3)  

#         self.le1.textChanged[str].connect(self.le1Changed)
#         self.le2.textChanged[str].connect(self.le2Changed)
#         self.le3.textChanged[str].connect(self.le3Changed)
#         self.le4.textChanged[str].connect(self.le4Changed)
#         self.le11.textChanged[str].connect(self.le11Changed)
#         self.le21.textChanged[str].connect(self.le21Changed)
#         self.le31.textChanged[str].connect(self.le31Changed)
#         self.le41.textChanged[str].connect(self.le41Changed)

#         btn1.clicked.connect(self.btn1_click)
#         btn2.clicked.connect(self.btn2_click)
#         btn3.clicked.connect(self.btn3_click)
      
#         grid = QGridLayout()
        
#         grid.addWidget(lb1 , 0, 0)
#         grid.addWidget(self.le1 , 0, 1)
#         grid.addWidget(lb11, 0, 2)
#         grid.addWidget(self.le11, 0, 3)

#         grid.addWidget(lb2 , 1, 0)
#         grid.addWidget(self.le2 , 1, 1)
#         grid.addWidget(lb21, 1, 2)
#         grid.addWidget(self.le21, 1, 3)

#         grid.addWidget(lb3 , 2, 0)
#         grid.addWidget(self.le3 , 2, 1)
#         grid.addWidget(lb31, 2, 2)
#         grid.addWidget(self.le31, 2, 3)

#         grid.addWidget(lb4 , 3, 0)
#         grid.addWidget(self.le4 , 3, 1)
#         grid.addWidget(lb41, 3, 2)
#         grid.addWidget(self.le41, 3, 3)
        
#         grid.addWidget(btn1 , 4, 1)
#         grid.addWidget(btn2, 4, 2)
#         grid.addWidget(btn3, 4, 3)
     
#         self.setLayout(grid)
#         # self.show()
    
#     def le1Changed(self, text):
#         self.cta_id = text
    
#     def le2Changed(self, text):
#         self.bs_id = text
    
#     def le3Changed(self, text):
#         self.super_id = text
    
#     def le4Changed(self, text):
#         self.cert_name = text
    
#     def le11Changed(self, text):
#         self.cta_pw = text
    
#     def le21Changed(self, text):
#         self.bs_pw = text
    
#     def le31Changed(self, text):
#         self.delay_time = text
    
#     def le41Changed(self, text):
#         self.cert_pw = text
    
#     def btn1_click(self):

#         # if self.le1.textChanged[str]!=True:
#         #     cta_id = self.cta_id
#         # elif self.le1.placeholderText()==nts_dict['secret']['세무사관리번호']:
#         #     cta_id = self.le1.placeholderText()
#         # else:
#         #     nts_dict['secret']['세무사관리번호']
        
#         # cta_id =  self.cta_id if self.le1.textChanged[str]!=True else self.le1.placeholderText() if self.le1.placeholderText()==nts_dict['secret']['세무사관리번호'] else nts_dict['secret']['세무사관리번호'] 
#         # bs_id =  self.bs_id if self.le2.textChanged[str]!=True else self.le2.placeholderText()
#         # super_id =  self.super_id if self.le3.textChanged[str]!=True else self.le3.placeholderText()
#         # cert_name =  self.cert_name if self.le4.textChanged[str]!=True else self.le4.placeholderText()
#         # cta_pw =  self.cta_pw if self.le11.textChanged[str]!=True else self.le11.placeholderText()
#         # bs_pw =  self.bs_pw if self.le21.textChanged[str]!=True else self.le21.placeholderText()
#         # delay_time =  self.delay_time if self.le31.textChanged[str]!=True else str(self.le31.placeholderText())
#         # cert_pw =  self.cert_pw if self.le41.textChanged[str]!=True else self.le41.placeholderText()


#         cta_id =  self.cta_id if self.le1.textChanged[str]!=True else self.le1.placeholderText()
#         bs_id =  self.bs_id if self.le2.textChanged[str]!=True else self.le2.placeholderText()
#         super_id =  self.super_id if self.le3.textChanged[str]!=True else self.le3.placeholderText()
#         cert_name =  self.cert_name if self.le4.textChanged[str]!=True else self.le4.placeholderText()
#         cta_pw =  self.cta_pw if self.le11.textChanged[str]!=True else self.le11.placeholderText()
#         bs_pw =  self.bs_pw if self.le21.textChanged[str]!=True else self.le21.placeholderText()
#         delay_time =  self.delay_time if self.le31.textChanged[str]!=True else str(self.le31.placeholderText())
#         cert_pw =  self.cert_pw if self.le41.textChanged[str]!=True else self.le41.placeholderText()
#         # 2. 수정된 딕셔너리를 json 파일로 만들어 저장      
#         with open(setdata.full_json_fn, 'w', encoding='utf-8') as fn:
#             nts_dict['secret']['세무사관리번호'] = cta_id
#             nts_dict['secret']['부서아이디'] = bs_id
#             nts_dict['secret']['수퍼아이디'] = super_id
#             nts_dict['secret']['공인인증서명칭'] = cert_name
#             nts_dict['secret']['세무사비번'] = cta_pw
#             nts_dict['secret']['부서비번'] = bs_pw            
#             nts_dict['secret']['딜레이타임'] = str(delay_time)
#             nts_dict['secret']['공인인증서비번'] = cert_pw
#             json.dump(nts_dict, fn, ensure_ascii=False, indent=4)
        
#         self.le1.setPlaceholderText(nts_dict['secret']['세무사관리번호'])
#         self.le2.setPlaceholderText(nts_dict['secret']['부서아이디'])
#         self.le3.setPlaceholderText(nts_dict['secret']['수퍼아이디'])
#         self.le4.setPlaceholderText(nts_dict['secret']['공인인증서명칭'])

#         self.le11.setPlaceholderText(nts_dict['secret']['세무사비번'])
#         self.le21.setPlaceholderText(nts_dict['secret']['부서비번'])
#         self.le31.setPlaceholderText(str(nts_dict['secret']['딜레이타임']))
#         self.le41.setPlaceholderText(nts_dict['secret']['공인인증서비번'])

#         # # 다른 창과 상호작용  https://freeprog.tistory.com/351 
#         # https://wikidocs.net/5249     
#         # inst = Ui_nts_login()
#         # # inst.exec_()
#         # inst.reload()
#         # self.close()
#         # # inst.close()

#         # https://www.riverbankcomputing.com/static/Docs/PyQt5/signals_slots.html#PyQt5.QtCore.pyqtSignal
#         # valueChanged = pyqtSignal(['QString'],['QString'])

        
#         # Ui_nts_login().le1Changed(self.bs_id)
#         # Ui_nts_login().le1Changed(str(self.delay_time))
    
#     def btn2_click(self):
#         pass
    
#     def btn3_click(self):
#         pass

class Ui_SettingMenu(QDialog):
    def __init__(self, parent=None):
        super().__init__()

        # 우하단 위젯   # self.setGeometry(300,300,500,10)
        rect = QDesktopWidget().availableGeometry()   # 작업표시줄 제외한 화면크기 반환 # .screenGeometry() : 화면해상도 class (0, 0, x, y)
        max_x = rect.width()
        max_y = rect.height()

        width, height = 500 , 155
        left = max_x - width 
        top = max_y - height 

        self.setGeometry(left, top-250, width, height)
        self.setWindowTitle("기본사항 저장(변경)")

        self.le1 = QLineEdit()
        self.le2 = QLineEdit()
        self.le3 = QLineEdit()
        self.le4 = QLineEdit()
        self.btn1 = QPushButton("변경사항 저장")

        flo1 = QFormLayout()
        flo1.addRow('세무사관리번호', self.le1)
        flo1.addRow('부서아이디', self.le2)
        flo1.addRow('홈택스대표아이디', self.le3)
        flo1.addRow('공인인증서명칭', self.le4)
        flo1.addRow(self.btn1)

        self.le11 = QLineEdit()
        self.le21 = QLineEdit()
        self.le31 = QLineEdit()
        self.le41 = QLineEdit()
        self.btn2 = QPushButton("인증서선택")
        self.btn3 = QPushButton("인증서정보저장")
        
        flo2 = QFormLayout()
        flo2.addRow('세무사비번', self.le11)
        flo2.addRow('부서비번', self.le21)
        flo2.addRow('딜레이타임', self.le31)
        flo2.addRow('인증서비번', self.le41)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.btn2)      
        hbox1.addWidget(self.btn3)
        flo2.addRow(hbox1)

        hbox2 = QHBoxLayout()
        hbox2.addLayout(flo1)      # 주의 addWidget 아님
        hbox2.addLayout(flo2)      # 주의 addWidget 아님

        self.setLayout(hbox2)

        # 입력제한 http://bitly.kr/wmonM2
        reg_ex = QRegExp("[0-9]+.?[0-9]{,2}")
        input_validator = QRegExpValidator(reg_ex, self.le31)
        # double_validator = QDoubleValidator(-999.0, 999.0, 2)   ### http://bitly.kr/wmonM2
        self.le31.setValidator(input_validator)      # double_validator)  
        self.le31.setMaxLength(3)  
        self.le31.setToolTip('홈택스 과부하로 로그인이 <br> 원할하지 않은 경우 1 또는 1.5 <br> 평상시 0.8 권장합니다.')

        self.le31.setStyleSheet(
                """QLineEdit { background-color: #f0f0f0; color: blue; font: bold }""")
        self.le4.setStyleSheet(
                """QLineEdit { background-color: #f0f0f0; color: blue }""")
        self.le41.setStyleSheet(
                """QLineEdit { background-color: #f0f0f0; color: blue }""")
        self.btn1.setStyleSheet(
                """QPushButton { color: blue; font: bold }""")

        # json 파일에서 불러온 딕셔너리 값으로 초기값 셋팅
        self.setup_value()

    def setup_value(self):
       
        self.le1.setPlaceholderText(nts_dict['secret']['세무사관리번호'])
        self.le2.setPlaceholderText(nts_dict['secret']['부서아이디'])
        self.le3.setPlaceholderText(nts_dict['secret']['수퍼아이디'])
        self.le4.setPlaceholderText(nts_dict['secret']['공인인증서명칭'])

        self.le11.setPlaceholderText(nts_dict['secret']['세무사비번'])
        self.le21.setPlaceholderText(nts_dict['secret']['부서비번'])
        self.le31.setPlaceholderText(str(nts_dict['secret']['딜레이타임']))
        self.le41.setPlaceholderText(nts_dict['secret']['공인인증서비번'])

        # self.show()
class ChangedVal:
    def __init__(self):
        cta_id = ""
        bs_id = ""
        delay_time = ""

class SettingMenu(Ui_SettingMenu):
    send_instance_signal = pyqtSignal("PyQt_PyObject")

    def __init__(self, parent=None):
        super().__init__(parent)

        self.cta_id = nts_dict['secret']['세무사관리번호']
        self.bs_id = nts_dict['secret']['부서아이디']
        self.super_id = nts_dict['secret']['수퍼아이디'] 
        self.cert_name = nts_dict['secret']['공인인증서명칭']
        self.cta_pw = nts_dict['secret']['세무사비번']
        self.bs_pw = nts_dict['secret']['부서비번'] 
        self.delay_time = str(nts_dict['secret']['딜레이타임']) 
        self.cert_pw = nts_dict['secret']['공인인증서비번'] 

        # connecting signal to slot 
        self.le1.textChanged[str].connect(self.cta_id_changed)
        self.le2.textChanged[str].connect(self.bs_id_changed)
        self.le3.textChanged[str].connect(self.super_id_changed)
        self.le4.textChanged[str].connect(self.cert_name_changed)
        self.le11.textChanged[str].connect(self.cta_pw_changed)
        self.le21.textChanged[str].connect(self.bs_pw_changed)
        self.le31.textChanged[str].connect(self.delay_time_changed)
        self.le41.textChanged[str].connect(self.cert_pw_changed)

        self.btn1.clicked.connect(self.save_changed_values)
        self.btn2.clicked.connect(self.select_cert)
        self.btn3.clicked.connect(self.save_cert)

        self.ntslog = Ui_nts_login(parent=self)
        self.send_instance_signal.connect(self.ntslog.receive_instance_signal)

        self.show()

    @pyqtSlot(str)
    def cta_id_changed(self, text):
        self.cta_id = text

    @pyqtSlot(str)
    def bs_id_changed(self, text):
        self.bs_id = text

    @pyqtSlot(str)
    def super_id_changed(self, text):
        self.super_id = text

    @pyqtSlot(str)
    def cert_name_changed(self, text):
        self.cert_name = text

    @pyqtSlot(str)
    def cta_pw_changed(self, text):
        self.cta_pw = text

    @pyqtSlot(str)
    def bs_pw_changed(self, text):
        self.bs_pw = text

    @pyqtSlot(str)
    def delay_time_changed(self, text):
        self.delay_time = text

    @pyqtSlot(str)
    def cert_pw_changed(self, text):
        self.cert_pw = text

    @pyqtSlot()
    def save_changed_values(self):

        cta_id =  self.cta_id if self.le1.textChanged[str]!=True else self.le1.placeholderText()
        bs_id =  self.bs_id if self.le2.textChanged[str]!=True else self.le2.placeholderText()
        super_id =  self.super_id if self.le3.textChanged[str]!=True else self.le3.placeholderText()
        cert_name =  self.cert_name if self.le4.textChanged[str]!=True else self.le4.placeholderText()
        cta_pw =  self.cta_pw if self.le11.textChanged[str]!=True else self.le11.placeholderText()
        bs_pw =  self.bs_pw if self.le21.textChanged[str]!=True else self.le21.placeholderText()
        delay_time =  self.delay_time if self.le31.textChanged[str]!=True else str(self.le31.placeholderText())
        cert_pw =  self.cert_pw if self.le41.textChanged[str]!=True else self.le41.placeholderText()
        # 2. 수정된 딕셔너리를 json 파일로 만들어 저장      
        with open(setdata.full_json_fn, 'w', encoding='utf-8') as fn:
            nts_dict['secret']['세무사관리번호'] = cta_id
            nts_dict['secret']['부서아이디'] = bs_id
            nts_dict['secret']['수퍼아이디'] = super_id
            nts_dict['secret']['공인인증서명칭'] = cert_name
            nts_dict['secret']['세무사비번'] = cta_pw
            nts_dict['secret']['부서비번'] = bs_pw            
            nts_dict['secret']['딜레이타임'] = str(delay_time)
            nts_dict['secret']['공인인증서비번'] = cert_pw
            json.dump(nts_dict, fn, ensure_ascii=False, indent=4)
        
        changed_values = ChangedVal()  
        changed_values.cta_id = nts_dict['secret']['세무사관리번호']
        changed_values.bs_id = nts_dict['secret']['부서아이디']
        changed_values.delay_time = nts_dict['secret']['딜레이타임']
        self.close()
        self.send_instance_signal.emit(changed_values)



    
    def select_cert(self):
        pass

    def save_cert(self):
        pass

class Ui_nts_login(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # super(QWidget,self).__init__(parent)
        self.bs_id = nts_dict['secret']['부서아이디']   
        # self.delay_time = float(nts_dict['secret']['딜레이타임'])
        self.delay_time = (nts_dict['secret']['딜레이타임']) if nts_dict['secret']['딜레이타임']!=False else 0.8
            
        self.initUI()

    def initUI(self):

        groupbox1 = QGroupBox('CTA ID 로그인')
        self.radio1 = QRadioButton('W15960')
        self.radio2 = QRadioButton('P27687')
        self.radio1.setChecked(True)

        # QRadioButton 예제 https://wikidocs.net/5237
        self.radio1.clicked.connect(self.radioButtonClicked)
        self.radio2.clicked.connect(self.radioButtonClicked)

        btn1 = QPushButton('홈택스 로그인')
        btn1.setToolTip('HomeTax Login')
        btn1.clicked.connect(self.btn1_click)

        vbox = QVBoxLayout()
        vbox.addWidget(self.radio1)
        vbox.addWidget(self.radio2)
        vbox.addWidget(btn1)
        groupbox1.setLayout(vbox)

        # return groupbox

    # def secondGroup(self):
        # QLineEdit 총괄 : https://www.tutorialspoint.com/pyqt/pyqt_qlineedit_widget
        groupbox2 = QGroupBox('부서 ID 및 딜레이 변경 ')

        self.le1 = QLineEdit()
        self.le2 = QLineEdit()
        self.le1.setPlaceholderText(nts_dict['secret']['부서아이디'])
        self.le2.setPlaceholderText(str(nts_dict['secret']['딜레이타임']))
      
        # 입력제한 http://bitly.kr/wmonM2
        reg_ex = QRegExp("[0-9]+.?[0-9]{,2}")
        input_validator = QRegExpValidator(reg_ex, self.le2)
        # double_validator = QDoubleValidator(-999.0, 999.0, 2)   ### http://bitly.kr/wmonM2
        self.le2.setValidator(input_validator)      # double_validator)  
        self.le2.setMaxLength(3)  

        self.le1.textChanged[str].connect(self.le1Changed)
        self.le2.textChanged[str].connect(self.le2Changed)

        btn2 = QPushButton('변경사항저장', self)
        btn2.setToolTip('저장하기')
        btn2.clicked.connect(self.btn2_click)

        flo = QFormLayout()
        flo.addRow("부서아이디", self.le1)
        flo.addRow("딜레이타임", self.le2)
        flo.addRow(btn2)
        groupbox2.setLayout(flo)
# ////////////
        hbox = QHBoxLayout(self)
        hbox.addWidget(groupbox1)
        hbox.addWidget(groupbox2)
        self.setLayout(hbox)


        # self.grid = QGridLayout(self)
        # # self.grid.addWidget(self.firstGroup(), 0, 0)
        # # self.grid.addWidget(self.secondGroup(), 0, 1)
        # self.grid.addWidget(groupbox1, 0, 0)
        # self.grid.addWidget(groupbox2, 0, 1)

        # self.setLayout(self.grid)
       
    # # def firstGroup(self):
    #     groupbox1 = QGroupBox('CTA ID 로그인')
    #     self.radio1 = QRadioButton('W15960')
    #     self.radio2 = QRadioButton('P27687')
    #     self.radio1.setChecked(True)

    #     # QRadioButton 예제 https://wikidocs.net/5237
    #     self.radio1.clicked.connect(self.radioButtonClicked)
    #     self.radio2.clicked.connect(self.radioButtonClicked)

    #     btn1 = QPushButton('홈택스 로그인')
    #     btn1.setToolTip('HomeTax Login')
    #     btn1.clicked.connect(self.btn1_click)

    #     vbox = QVBoxLayout()
    #     vbox.addWidget(self.radio1)
    #     vbox.addWidget(self.radio2)
    #     vbox.addWidget(btn1)
    #     groupbox1.setLayout(vbox)

    #     # return groupbox

    # # def secondGroup(self):
    #     # QLineEdit 총괄 : https://www.tutorialspoint.com/pyqt/pyqt_qlineedit_widget
    #     groupbox2 = QGroupBox('부서 ID 및 딜레이 변경 ')

    #     self.le1 = QLineEdit()
    #     self.le2 = QLineEdit()
    #     self.le1.setPlaceholderText(nts_dict['secret']['부서아이디'])
    #     self.le2.setPlaceholderText(str(nts_dict['secret']['딜레이타임']))
      
    #     # 입력제한 http://bitly.kr/wmonM2
    #     reg_ex = QRegExp("[0-9]+.?[0-9]{,2}")
    #     input_validator = QRegExpValidator(reg_ex, self.le2)
    #     # double_validator = QDoubleValidator(-999.0, 999.0, 2)   ### http://bitly.kr/wmonM2
    #     self.le2.setValidator(input_validator)      # double_validator)  
    #     self.le2.setMaxLength(3)  

    #     self.le1.textChanged[str].connect(self.le1Changed)
    #     self.le2.textChanged[str].connect(self.le2Changed)

    #     btn2 = QPushButton('변경사항저장', self)
    #     btn2.setToolTip('저장하기')
    #     btn2.clicked.connect(self.btn2_click)

    #     flo = QFormLayout()
    #     flo.addRow("부서아이디", self.le1)
    #     flo.addRow("딜레이타임", self.le2)
    #     flo.addRow(btn2)
    #     groupbox2.setLayout(flo)

    #     # return groupbox

    def radioButtonClicked(self):
      
        if self.radio1.isChecked():
            if self.radio1.text() != nts_dict['secret']['세무사관리번호']:
                nts_dict['secret']['세무사관리번호'] = self.radio1.text()
                
        elif self.radio2.isChecked():
            if self.radio2.text() != nts_dict['secret']['세무사관리번호']:
                nts_dict['secret']['세무사관리번호'] = self.radio2.text()
        else:
            pass
        # 2. 수정된 딕셔너리를 json 파일로 만들어 저장      
        with open(setdata.full_json_fn, 'w', encoding='utf-8') as fn:
            json.dump(nts_dict, fn, ensure_ascii=False, indent=4)
    
    def btn1_click(self):
        if self.radio1.isChecked():
            if self.radio1.text() != nts_dict['secret']['세무사관리번호']:
                nts_dict['secret']['세무사관리번호'] = self.radio1.text()
                
        elif self.radio2.isChecked():
            if self.radio2.text() != nts_dict['secret']['세무사관리번호']:
                nts_dict['secret']['세무사관리번호'] = self.radio2.text()
        else:
            pass
        # 2. 수정된 딕셔너리를 json 파일로 만들어 저장      
        with open(setdata.full_json_fn, 'w', encoding='utf-8') as fn:
            json.dump(nts_dict, fn, ensure_ascii=False, indent=4)

        # 홈택스 로그인
        login = hometax.Nts_Login()
        login.path2()

    def le1Changed(self, text):
        self.bs_id = text
      
    def le2Changed(self, text):
        self.delay_time = text
       
    def btn2_click(self):
        # bs_id =  self.bs_id if self.le1.textChanged[str]==True else self.le1.text()
        # delay_time =  self.delay_time if self.le2.textChanged[str]==True else str(0.8)
        print(type(self.le1.textChanged[str]))
        
        # print(self.le1.textChanged[str].text())
        bs_id =  self.bs_id if self.le1.textChanged[str]!=True else self.le1.placeholderText()              # nts_dict['secret']['부서아이디']
        delay_time =  self.delay_time if self.le2.textChanged[str]!=True else self.le2.placeholderText()    # nts_dict['secret']['딜레이타임']
        # 2. 수정된 딕셔너리를 json 파일로 만들어 저장      
        with open(setdata.full_json_fn, 'w', encoding='utf-8') as fn:
            nts_dict['secret']['부서아이디'] = bs_id
            nts_dict['secret']['딜레이타임'] = str(delay_time)
            json.dump(nts_dict, fn, ensure_ascii=False, indent=4)
        
        self.le1.setPlaceholderText(nts_dict['secret']['부서아이디'])
        self.le2.setPlaceholderText(str(nts_dict['secret']['딜레이타임']))
    
    @pyqtSlot("PyQt_PyObject")
    def receive_instance_signal(self, inst):
        print(inst.bs_id)
        print(inst.delay_time)
        print(self.le1.text())
        # self.le1.setText(inst.bs_id)
        # self.le2.setText(str(inst.delay_time))
        print(self.le1.placeholderText())
        self.le1.setPlaceholderText(inst.bs_id)
        self.le2.setPlaceholderText(str(inst.delay_time))

class Ui_nts_task(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        # super(QWidget,self).__init__(parent)
        
        self.initUi()

    def initUi(self):

        grid = QGridLayout()
        btn1 = QPushButton()
        grid.addWidget(btn1)
        btn1.clicked.connect(self.btn1_click)

        self.setLayout(grid) 

    def btn1_click(self):
        print("btn1 clicked") 
        driver = driverutil.IE_driver(r'C:\zz\NTS\driver', 'IEDriverServer.exe')
        driver = driver.set_driver()


class Ui_web_task(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        # super(QWidget,self).__init__(parent) 
        label = QLabel('개발중...') 
        layout = QVBoxLayout()
        layout.addWidget(label) 

        self.setLayout(layout)  
# class Ui_Main(QMainWindow):
#         """ QMainWindow 에서는 QHBoxLayout, QVBoxLayout 같은 layout 사용못함.
#             QWidget, QDialog 와 달리 QMainWindow 는 자체적으로 layout 가지고 있다. central widget 을 반드시 필요로함.
#             https://freeprog.tistory.com/326"""
#     def __init__(self, parent=None):    
#         super().__init__(parent)

class Main(QMainWindow):  # (QWidget): #
    def __init__(self):
        """ QMainWindow 에서는 QHBoxLayout, QVBoxLayout 같은 layout 사용못함.
            QWidget, QDialog 와 달리 QMainWindow 는 자체적으로 layout 가지고 있다. central widget 을 반드시 필요로함.
            https://freeprog.tistory.com/326"""
        super().__init__()
        
        # self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowTitleHint)  # | Qt.FramelessWindowHint)  항상 위에
        # 우하단 위젯
        # rect = QDesktopWidget().screenGeometry()    # 화면해상도   class (0, 0, x, y) 
        rect = QDesktopWidget().availableGeometry()   # 작업표시줄 제외한 화면크기 반환
        max_x = rect.width()
        max_y = rect.height()

        width, height = 350 , 220
        # width, height = 350 , 250
        left = max_x - width 
        top = max_y - height 

        self.setGeometry(left, top, width, height)

        # 탭 위젯
        tab1 = Ui_nts_login(self)
        tab2 = Ui_nts_task(self)
        tab3 = Ui_web_task(self)

        tabs = QTabWidget()
        tabs.addTab(tab1, '홈택스 로그인')
        tabs.addTab(tab2, '홈택스 작업')
        tabs.addTab(tab3, '웹 작업')

        self.setCentralWidget(tabs)         
        self.setWindowTitle('ATM(자동화)')
        self.setWindowFlags(Qt.FramelessWindowHint)   # windowtitle 제외

        #>>> 메뉴바 https://wikidocs.net/21866  
        # 메뉴바 위젯연결 https://stackoverflow.com/questions/45688873/pyqt5-click-menu-and-open-new-window
        setAction = QAction(QIcon('exit.png'), '기본사항 저장(변경)', self)
        # setAction.setShortcut('Ctrl+Q')
        setAction.setStatusTip('기본사항 저장(변경)...')
        setAction.triggered.connect(self.id_setting)

        exitAction = QAction(QIcon('exit.png'), '종료', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        # self.statusBar()

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('&메뉴')
        fileMenu.addAction(setAction)
        fileMenu.addAction(exitAction)
        #<<< 메뉴바
        self.statusBar().showMessage('Ready')

        # 인포텍 모쥴 설치 
        if (nts_dict['secret']['공인인증서명칭'] == "" or
            nts_dict['secret']['공인인증서비번'] == ""):

            if not os.path.isfile(r'C:\Infotech\Common\iftWinExAdapter.dll'):

                title = "공인인증서 모듈설치"
                msg = "지금 공인인증서 모듈을 설치하시겠습니까 ??<br>나중에 설치가능 합니다!!"
                inst = Util.MsgBoxTF(title, msg)
                TF = inst.initUI()

                if TF==True:
                    driverutil.setup_iftCertAdapter()  
                else:
                    pass

        self.show()

        # 공란인 변수 있으면 초기세팅
        if (nts_dict['secret']['세무사관리번호'] == "" or
            nts_dict['secret']['부서아이디'] == "" or
            nts_dict['secret']['공인인증서명칭'] == "" or
            nts_dict['secret']['세무사비번'] == "" or
            nts_dict['secret']['부서비번'] == "" or            
            nts_dict['secret']['딜레이타임'] == "" or
            nts_dict['secret']['공인인증서비번'] == ""):
        
            require_list = []
            for key, val in nts_dict['secret'].items():
                if val=="":
                    require_list.append(key)

            require_str = " / ".join(require_list)

            title = "필수사항 초기입력"
            msg = f"필수사항({require_str})입력이 필요합니다!!<br>지금 필수사항을 입력하시겠습니까??"
            inst = Util.MsgBoxTF(title, msg)
            TF = inst.initUI()

            if TF==True:
                self.id_setting()
            else:
                pass
    @pyqtSlot()
    def id_setting(self):
        
        widget = SettingMenu()
        # widget.save_changed_values()
        widget.exec_()

if __name__ == "__main__":
    print("*"*100)
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())
        
