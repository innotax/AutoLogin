import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDesktopWidget, QWidget, QDialog, 
                            QPushButton, QRadioButton, QLabel, QLineEdit, QAction, QToolTip, qApp)
from PyQt5.QtWidgets import QMessageBox, QTabWidget, QGridLayout, QGroupBox, QHBoxLayout, QVBoxLayout, QFormLayout
from PyQt5.QtGui import QIcon, QRegExpValidator, QDoubleValidator, QIntValidator, QFont
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QRegExp


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

class SettingMenu(Ui_SettingMenu):
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
        
        self.setup_value()   
    
    def select_cert(self):
        pass

    def save_cert(self):
        pass
   

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = SettingMenu()
    sys.exit(app.exec_())