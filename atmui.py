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
from utils import Util, driverutil, iftutil

# 변수의 스코프  https://umbum.tistory.com/823
nts_dict = hometax.nts_dict

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

        self.le_cta_id = QLineEdit()
        self.le_bs_id = QLineEdit()
        self.le_super_id = QLineEdit()
        self.le_cert_nm = QLineEdit()
        self.btn1 = QPushButton("변경사항 저장")

        flo1 = QFormLayout()
        flo1.addRow('세무사관리번호', self.le_cta_id)
        flo1.addRow('부서아이디', self.le_bs_id)
        flo1.addRow('홈택스대표아이디', self.le_super_id)
        flo1.addRow('공인인증서명칭', self.le_cert_nm)
        flo1.addRow(self.btn1)

        self.le_cta_pw = QLineEdit()
        self.le_bs_pw = QLineEdit()
        self.le_delay_time = QLineEdit()
        self.le_cert_pw = QLineEdit()
        self.btn2 = QPushButton("인증서선택(저장) ")
        
        flo2 = QFormLayout()
        flo2.addRow('세무사비번', self.le_cta_pw)
        flo2.addRow('부서비번', self.le_bs_pw)
        flo2.addRow('딜레이타임', self.le_delay_time)
        flo2.addRow('인증서비번', self.le_cert_pw)
        flo2.addRow(self.btn2)

        hbox2 = QHBoxLayout()
        hbox2.addLayout(flo1)      # 주의 addWidget 아님
        hbox2.addLayout(flo2)      # 주의 addWidget 아님

        self.setLayout(hbox2)

        # 입력제한 http://bitly.kr/wmonM2
        reg_ex = QRegExp("[0-9]+.?[0-9]{,2}")
        input_validator = QRegExpValidator(reg_ex, self.le_delay_time)
        # double_validator = QDoubleValidator(-999.0, 999.0, 2)   ### http://bitly.kr/wmonM2
        self.le_delay_time.setValidator(input_validator)      # double_validator)  
        self.le_delay_time.setMaxLength(3)  
        self.le_delay_time.setToolTip('홈택스 과부하로 로그인이 <br> 원할하지 않은 경우 1 또는 1.5 <br> 평상시 0.8 권장합니다.')

        # self.le_delay_time.setStyleSheet(
        #         """QLineEdit { background-color: #f0f0f0; color: blue; font: bold }""")
        self.le_cert_nm.setStyleSheet(
                """QLineEdit { background-color: #f0f0f0; color: blue; font: bold }""")
        self.le_cert_pw.setStyleSheet(
                """QLineEdit { background-color: #f0f0f0; color: blue; font: bold }""")
        self.btn1.setStyleSheet(
                """QPushButton { color: blue; font: bold }""")
        self.le_cert_nm.setReadOnly(True)
        self.le_cert_pw.setReadOnly(True)

        # self.show()

class SettingMenu(Ui_SettingMenu):
    # 1. Signal 객체를 담을 inst 생성
    cta_id_changed_signal = pyqtSignal(str)
    bs_id_changed_signal = pyqtSignal(str)
    delay_time_changed_signal = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)

        self.cta_id = nts_dict['secret']['세무사관리번호']
        self.bs_id = nts_dict['secret']['부서아이디']
        self.super_id = nts_dict['secret']['수퍼아이디'] 
        self.cert_nm = nts_dict['secret']['공인인증서명칭']
        self.cta_pw = nts_dict['secret']['세무사비번']
        self.bs_pw = nts_dict['secret']['부서비번'] 
        self.delay_time = str(nts_dict['secret']['딜레이타임']) 
        self.cert_pw = nts_dict['secret']['공인인증서비번'] 

        # connecting signal to slot 
        self.le_cta_id.editingFinished.connect(self.cta_id_changed)
        self.le_bs_id.editingFinished.connect(self.bs_id_changed)
        self.le_super_id.editingFinished.connect(self.super_id_changed)
        self.le_cert_nm.editingFinished.connect(self.cert_nm_changed)
        self.le_cta_pw.editingFinished.connect(self.cta_pw_changed)
        self.le_bs_pw.editingFinished.connect(self.bs_pw_changed)
        self.le_delay_time.editingFinished.connect(self.delay_time_changed)
        self.le_cert_pw.editingFinished.connect(self.cert_pw_changed)

        self.btn1.clicked.connect(self.save_changed_values)
        self.btn2.clicked.connect(self.select_cert)

        # json 파일에서 불러온 딕셔너리 값으로 초기값 셋팅
        self.set_placeholder()
        
    def set_placeholder(self):
       
        self.le_cta_id.setPlaceholderText(nts_dict['secret']['세무사관리번호'])
        self.le_bs_id.setPlaceholderText(nts_dict['secret']['부서아이디'])
        self.le_super_id.setPlaceholderText(nts_dict['secret']['수퍼아이디'])
        self.le_cert_nm.setPlaceholderText(nts_dict['secret']['공인인증서명칭'])

        self.le_cta_pw.setPlaceholderText(nts_dict['secret']['세무사비번'])
        self.le_bs_pw.setPlaceholderText(nts_dict['secret']['부서비번'])
        self.le_delay_time.setPlaceholderText(str(nts_dict['secret']['딜레이타임']))
        self.le_cert_pw.setPlaceholderText(nts_dict['secret']['공인인증서비번'])

    @pyqtSlot()
    def cta_id_changed(self):
        if (self.cta_id != self.le_cta_id.text() and   # value changed
            self.le_cta_id.text() != ""):              # value changed

            text = self.le_cta_id.text()
            self.cta_id = text
            nts_dict['secret']['세무사관리번호'] = text
            # 2. 수정된 딕셔너리를 json 파일로 만들어 저장      
            with open(setdata.full_json_fn, 'w', encoding='utf-8') as fn:
                json.dump(nts_dict, fn, ensure_ascii=False, indent=4)
            # 2. 시그널 객체 방출
            self.cta_id_changed_signal.emit(text)
        
    @pyqtSlot()
    def bs_id_changed(self):
        if (self.bs_id != self.le_bs_id.text() and
            self.le_bs_id.text() != ""):

            text = self.le_bs_id.text()
            self.bs_id = text
            nts_dict['secret']['부서아이디'] = text
            # 2. 수정된 딕셔너리를 json 파일로 만들어 저장      
            with open(setdata.full_json_fn, 'w', encoding='utf-8') as fn:
                json.dump(nts_dict, fn, ensure_ascii=False, indent=4)
            # 2. 시그널 객체 방출
            self.bs_id_changed_signal.emit(text)

    @pyqtSlot()
    def super_id_changed(self):
        if (self.super_id != self.le_super_id.text() and
            self.le_super_id.text() != ""):

            text = self.le_super_id.text()
            self.super_id = text
            nts_dict['secret']['수퍼아이디'] = text
            # 2. 수정된 딕셔너리를 json 파일로 만들어 저장      
            with open(setdata.full_json_fn, 'w', encoding='utf-8') as fn:
                json.dump(nts_dict, fn, ensure_ascii=False, indent=4)

    @pyqtSlot()
    def cert_nm_changed(self):
        if (self.cert_nm != self.le_cert_nm.text() and
            self.le_cert_nm.text() != ""):

            text = self.le_cert_nm.text()
            self.cert_nm = text
            nts_dict['secret']['공인인증서명칭'] = text
            # 2. 수정된 딕셔너리를 json 파일로 만들어 저장      
            with open(setdata.full_json_fn, 'w', encoding='utf-8') as fn:
                json.dump(nts_dict, fn, ensure_ascii=False, indent=4)

    @pyqtSlot()
    def cta_pw_changed(self):
        if (self.cta_pw != self.le_cta_pw.text() and
            self.le_cta_pw.text() != ""):

            text = self.le_cta_pw.text()
            self.cta_pw = text
            nts_dict['secret']['세무사비번'] = text
            # 2. 수정된 딕셔너리를 json 파일로 만들어 저장      
            with open(setdata.full_json_fn, 'w', encoding='utf-8') as fn:
                json.dump(nts_dict, fn, ensure_ascii=False, indent=4)

    @pyqtSlot()
    def bs_pw_changed(self):
        if (self.bs_pw != self.le_bs_pw.text() and
            self.le_bs_pw.text() != ""):
                
            text = self.le_bs_pw.text()
            self.bs_pw = text
            nts_dict['secret']['부서비번'] = text
            # 2. 수정된 딕셔너리를 json 파일로 만들어 저장  
            Util.save_dict_to_json(setdata.full_json_fn, nts_dict)

    @pyqtSlot()
    def delay_time_changed(self):
        if (self.delay_time != self.le_delay_time.text() and
            self.le_delay_time.text() !=""):

            text = self.le_delay_time.text()
            self.delay_time = text
            nts_dict['secret']['딜레이타임'] = text
            # 2. 수정된 딕셔너리를 json 파일로 만들어 저장  
            Util.save_dict_to_json(setdata.full_json_fn, nts_dict)
            # 2. 시그널 객체 방출
            self.delay_time_changed_signal.emit(text)

    @pyqtSlot()
    def cert_pw_changed(self):
        if (self.cert_pw != self.le_cert_pw.text() and
            self.le_cert_pw.text() !=""):

            text = self.le_cert_pw.text()
            self.cert_pw = text
            nts_dict['secret']['공인인증서비번'] = text
            # 2. 수정된 딕셔너리를 json 파일로 만들어 저장  
            Util.save_dict_to_json(setdata.full_json_fn, nts_dict)

    @pyqtSlot()
    def save_changed_values(self):

        nts_dict['secret']['세무사관리번호'] = self.cta_id
        nts_dict['secret']['부서아이디'] = self.bs_id
        nts_dict['secret']['수퍼아이디'] = self.super_id
        nts_dict['secret']['공인인증서명칭'] = self.cert_nm
        nts_dict['secret']['세무사비번'] = self.cta_pw
        nts_dict['secret']['부서비번'] = self.bs_pw            
        nts_dict['secret']['딜레이타임'] = str(self.delay_time)
        nts_dict['secret']['공인인증서비번'] = self.cert_pw

        # 2. 수정된 딕셔너리를 json 파일로 만들어 저장  
        Util.save_dict_to_json(setdata.full_json_fn, nts_dict)
        # setplaceholder QLineEdit
        self.set_placeholder()
        self.close()
    
    def select_cert(self):
        # 공인인증서 모듈 실행
        cert_nm, cert_pw = iftutil.cert_nm_pw()
        if cert_nm:            # 공인인증서 선택이 정상적이면  
            self.cert_nm = cert_nm
            self.cert_pw = cert_pw
            nts_dict['secret']['공인인증서명칭'] = cert_nm
            nts_dict['secret']['공인인증서비번'] = cert_pw
            # 2. 수정된 딕셔너리를 json 파일로 만들어 저장      
            with open(setdata.full_json_fn, 'w', encoding='utf-8') as fn:
                json.dump(nts_dict, fn, ensure_ascii=False, indent=4)

            self.set_placeholder()
    
    def make_connection(self, signal_emit_object):
        signal_emit_object.cta_id_changed_signal.connect(self.receive_cta_id)
    
    @pyqtSlot(str)
    def receive_cta_id(self, txt):
        self.le_cta_id.setText(txt)
        self.le_cta_id.setPlaceholderText(txt)

        cls_name = self.__class__.__name__            # class 이름
        func_name = sys._getframe().f_code.co_name    # func  이름
        print(f'Receive at >>> class : < {cls_name} > function : < {func_name} > !!!')
        # print('from {} receive'.format(self.__class__.__name__))
        print(txt)


class Ui_Main(QMainWindow):
    """ QMainWindow 에서는 QHBoxLayout, QVBoxLayout 같은 layout 사용못함.
        QWidget, QDialog 와 달리 QMainWindow 는 자체적으로 layout 가지고 있다. central widget 을 반드시 필요로함.
        https://freeprog.tistory.com/326"""
    def __init__(self, parent=None):
        super().__init__(parent)

        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget() 

        tab1.setLayout(self.tab1_layout())
        tab2.setLayout(self.tab2_layout())
        tab3.setLayout(self.tab3_layout())

        tabs = QTabWidget()
        tabs.addTab(tab1, "HomeTax")
        tabs.addTab(tab2, "2nd Tab")
        tabs.addTab(tab3, "3rd Tab")

        self.setCentralWidget(tabs)
        self.setWindowTitle("자동로그인 !!!")
        # self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowTitleHint)  # | Qt.FramelessWindowHint)  항상 위에
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


    def tab1_layout(self):
        self.le_cta_id = QLineEdit()
        self.le_bs_id = QLineEdit()
        self.le_delay_time = QLineEdit()
        self.btn_login = QPushButton("로그인")

        self.btn_login.setStyleSheet(
                """QPushButton { background-color: #ffff00; color: blue; font: bold }""")       

        # 입력제한 http://bitly.kr/wmonM2
        reg_ex = QRegExp("[0-9]+.?[0-9]{,2}")
        input_validator = QRegExpValidator(reg_ex, self.le_delay_time)
        # double_validator = QDoubleValidator(-999.0, 999.0, 2)   ### http://bitly.kr/wmonM2
        self.le_delay_time.setValidator(input_validator)      # double_validator)  
        self.le_delay_time.setMaxLength(3) 

        flo1 = QFormLayout()
        flo1.addRow("세무사관리번호", self.le_cta_id)
        flo1.addRow("부서아이디", self.le_bs_id)
        flo1.addRow("딜레이타임", self.le_delay_time)
        flo1.addRow(self.btn_login)

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


class Main(Ui_Main):

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.cta_id = nts_dict['secret']['세무사관리번호']
        self.bs_id = nts_dict['secret']['부서아이디']
        self.super_id = nts_dict['secret']['수퍼아이디'] 
        self.cert_nm = nts_dict['secret']['공인인증서명칭']
        self.cta_pw = nts_dict['secret']['세무사비번']
        self.bs_pw = nts_dict['secret']['부서비번'] 
        self.delay_time = str(nts_dict['secret']['딜레이타임']) 
        self.cert_pw = nts_dict['secret']['공인인증서비번'] 

        if (self.cert_nm == "" or
            self.cert_pw == ""):

            title = "공인인증서 등록"
            msg = f"홈택스 로그인 시 공인인증서 정보가 필요합니다 !!!<br>지금 등록 하시겠습니까??"
            inst = Util.MsgBoxTF(title, msg)
            TF = inst.initUI()

            if TF==True:
                self.setup_iftAdapter()
            else:
                pass        
        
        if (self.cta_id=="" or self.cta_pw=="" ):
            # require_list = []
            # for key, val in nts_dict['secret'].items():
            #     if val=="":
            #         require_list.append(key)
            # require_str = " / ".join(require_list)

            title = "필수사항 초기입력"
            # msg = f"필수사항({require_str})입력이 필요합니다!!<br>지금 필수사항을 입력하시겠습니까??"
            msg = f"세무법인은 세무사관리번호, 세무사관리번호 비밀번호는 반드시 입력해야 합니다 !!<br>지금 필수사항을 입력하시겠습니까??"
            inst = Util.MsgBoxTF(title, msg)
            TF = inst.initUI()

            if TF==True:
                setting = SettingMenu()
                setting.exec_()
            else:
                pass

        self.set_placeholder() 

        # Signal connect Slot
        self.le_cta_id.editingFinished.connect(self.cta_id_changed) 
        self.le_bs_id.editingFinished.connect(self.bs_id_changed) 
        self.le_delay_time.editingFinished.connect(self.delay_time_changed) 
        self.btn_login.clicked.connect(self.login_clicked)

        self.show()

    def set_placeholder(self):
        self.le_cta_id.setPlaceholderText(nts_dict['secret']['세무사관리번호'])
        self.le_bs_id.setPlaceholderText(nts_dict['secret']['부서아이디'])
        self.le_delay_time.setPlaceholderText(str(nts_dict['secret']['딜레이타임']))

    def setup_iftAdapter(self):
        if not os.path.isfile(r'C:\Infotech\Common\iftWinExAdapter.dll'):  # 인포텍모듈 없으면
            title = "공인인증서 모듈설치"
            msg = "지금 공인인증서 모듈을 설치하시겠습니까 ??<br>나중에 설치가능 합니다!!"
            inst = Util.MsgBoxTF(title, msg)
            TF = inst.initUI()
            if TF==True:
                driverutil.setup_iftCertAdapter()  
            else:
                pass
        elif os.path.isfile(r'C:\Infotech\Common\iftWinExAdapter.dll'):    # 인포텍모듈 있으면
            # 공인인증서 모듈 실행
            cert_nm, cert_pw = iftutil.cert_nm_pw()
            self.cert_nm = cert_nm
            self.cert_pw = cert_pw
            nts_dict['secret']['공인인증서명칭'] = cert_nm
            nts_dict['secret']['공인인증서비번'] = cert_pw

            # 2. 수정된 딕셔너리를 json 파일로 만들어 저장      
            with open(setdata.full_json_fn, 'w', encoding='utf-8') as fn:
                json.dump(nts_dict, fn, ensure_ascii=False, indent=4)

    @pyqtSlot()
    def cta_id_changed(self):
        if (self.cta_id != self.le_cta_id.text() and   # value changed
            self.le_cta_id.text() != ""):              # value changed

            text = self.le_cta_id.text()
            self.cta_id = text
            nts_dict['secret']['세무사관리번호'] = text
            # 2. 수정된 딕셔너리를 json 파일로 만들어 저장      
            with open(setdata.full_json_fn, 'w', encoding='utf-8') as fn:
                json.dump(nts_dict, fn, ensure_ascii=False, indent=4)
        
    @pyqtSlot()
    def bs_id_changed(self):
        if (self.bs_id != self.le_bs_id.text() and
            self.le_bs_id.text() != ""):

            text = self.le_bs_id.text()
            self.bs_id = text
            nts_dict['secret']['부서아이디'] = text
            # 2. 수정된 딕셔너리를 json 파일로 만들어 저장      
            with open(setdata.full_json_fn, 'w', encoding='utf-8') as fn:
                json.dump(nts_dict, fn, ensure_ascii=False, indent=4)

    @pyqtSlot()
    def delay_time_changed(self):
        if (self.delay_time != self.le_delay_time.text() and
            self.le_delay_time.text() !=""):

            text = self.le_delay_time.text()
            self.delay_time = text
            nts_dict['secret']['딜레이타임'] = text
            # 2. 수정된 딕셔너리를 json 파일로 만들어 저장  
            Util.save_dict_to_json(setdata.full_json_fn, nts_dict)

    @pyqtSlot()
    def login_clicked(self):
        print(self.le_cta_id.placeholderText())
        if self.cta_id != self.le_cta_id.placeholderText():
            nts_dict['secret']['세무사관리번호'] = self.le_cta_id.placeholderText()
        if self.bs_id != self.le_cta_id.placeholderText():
            nts_dict['secret']['부서아이디'] = self.le_bs_id.placeholderText()
        if self.delay_time != self.le_delay_time.placeholderText():
            nts_dict['secret']['딜레이타임'] = str(self.le_delay_time.placeholderText())

        if self.le_cta_id.text() != "":
            nts_dict['secret']['세무사관리번호'] = self.le_cta_id.text()
        if self.le_bs_id.text() != "":
            nts_dict['secret']['부서아이디'] = self.le_bs_id.text()
        if self.le_delay_time.text() != "":
            nts_dict['secret']['딜레이타임'] = str(self.le_delay_time.text())
        

        # nts_dict['secret']['세무사관리번호'] = self.cta_id
        # nts_dict['secret']['부서아이디'] = self.bs_id       
        # nts_dict['secret']['딜레이타임'] = str(self.delay_time)
        # 2. 수정된 딕셔너리를 json 파일로 만들어 저장  
        Util.save_dict_to_json(setdata.full_json_fn, nts_dict)
        # setplaceholder QLineEdit
        self.set_placeholder()
        # 홈택스 로그인
        login = hometax.Nts_Login()
        login.path2()


    @pyqtSlot()
    def id_setting(self):       
        widget = SettingMenu()
        self.make_connection(widget)
        widget.exec_()

    def make_connection(self, signal_emit_object):
        signal_emit_object.cta_id_changed_signal.connect(self.receive_cta_id)
        signal_emit_object.bs_id_changed_signal.connect(self.receive_bs_id)
        signal_emit_object.delay_time_changed_signal.connect(self.receive_delay_time)

    
    @pyqtSlot(str)
    def receive_cta_id(self, txt):
        self.le_cta_id.setText(txt)
        self.le_cta_id.setPlaceholderText(txt)

    @pyqtSlot(str)
    def receive_bs_id(self, txt):
        self.le_bs_id.setText(txt)
        self.le_bs_id.setPlaceholderText(txt)

    @pyqtSlot(str)
    def receive_delay_time(self, txt):
        self.le_delay_time.setText(txt)
        self.le_delay_time.setPlaceholderText(txt)


if __name__ == "__main__":
    print("*"*100)
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())
        
