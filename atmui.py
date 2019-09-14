import os, sys, time, json, zipfile, subprocess

import PyQt5
# from PyQt5.Qt import QApplication
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDesktopWidget, QWidget, QDialog, QComboBox, QInputDialog,
                            QPushButton, QRadioButton, QLabel, QLineEdit, QAction, QToolTip, qApp)
from PyQt5.QtWidgets import QMessageBox, QTabWidget, QGridLayout, QGroupBox, QHBoxLayout, QVBoxLayout, QFormLayout
from PyQt5.QtGui import QIcon, QRegExpValidator, QDoubleValidator, QIntValidator, QFont ,QPixmap
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QRegExp

# 상위폴더 내 파일 import  https://brownbears.tistory.com/296
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from data import setdata, dictdata
from sites import hometax, website
from utils import Util, driverutil, iftutil

# ===== Config =====
# 변수의 스코프  https://umbum.tistory.com/823
nts_dict = hometax.nts_dict
web_dict = hometax.web_dict
FULLPATH_NTS_JSON = setdata.FULLPATH_NTS_JSON
FULLPATH_WEB_JSON = setdata.FULLPATH_WEB_JSON
jsconverter = Util.JsonConverter()
## ==================

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
            jsconverter.dict_to_json(nts_dict, FULLPATH_NTS_JSON)
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
            jsconverter.dict_to_json(nts_dict, FULLPATH_NTS_JSON)
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
            jsconverter.dict_to_json(nts_dict, FULLPATH_NTS_JSON)

    @pyqtSlot()
    def cert_nm_changed(self):
        if (self.cert_nm != self.le_cert_nm.text() and
            self.le_cert_nm.text() != ""):

            text = self.le_cert_nm.text()
            self.cert_nm = text
            nts_dict['secret']['공인인증서명칭'] = text
            # 2. 수정된 딕셔너리를 json 파일로 만들어 저장      
            jsconverter.dict_to_json(nts_dict, FULLPATH_NTS_JSON)

    @pyqtSlot()
    def cta_pw_changed(self):
        if (self.cta_pw != self.le_cta_pw.text() and
            self.le_cta_pw.text() != ""):

            text = self.le_cta_pw.text()
            self.cta_pw = text
            nts_dict['secret']['세무사비번'] = text
            # 2. 수정된 딕셔너리를 json 파일로 만들어 저장      
            jsconverter.dict_to_json(nts_dict, FULLPATH_NTS_JSON)

    @pyqtSlot()
    def bs_pw_changed(self):
        if (self.bs_pw != self.le_bs_pw.text() and
            self.le_bs_pw.text() != ""):
                
            text = self.le_bs_pw.text()
            self.bs_pw = text
            nts_dict['secret']['부서비번'] = text
            # 2. 수정된 딕셔너리를 json 파일로 만들어 저장  
            jsconverter.dict_to_json(nts_dict, FULLPATH_NTS_JSON)

    @pyqtSlot()
    def delay_time_changed(self):
        if (self.delay_time != self.le_delay_time.text() and
            self.le_delay_time.text() !=""):

            text = self.le_delay_time.text()
            self.delay_time = text
            nts_dict['secret']['딜레이타임'] = text
            # 2. 수정된 딕셔너리를 json 파일로 만들어 저장  
            jsconverter.dict_to_json(nts_dict, FULLPATH_NTS_JSON)
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
            jsconverter.dict_to_json(nts_dict, FULLPATH_NTS_JSON)

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
        jsconverter.dict_to_json(nts_dict, FULLPATH_NTS_JSON)
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
            jsconverter.dict_to_json(nts_dict, FULLPATH_NTS_JSON)

            self.set_placeholder()
    
    def make_connection(self, signal_emit_object):
        signal_emit_object.cta_id_changed_signal.connect(self.receive_cta_id)
    
    @pyqtSlot(str)
    def receive_cta_id(self, txt):
        self.le_cta_id.setText(txt)
        self.le_cta_id.setPlaceholderText(txt)

        # cls_name = self.__class__.__name__            # class 이름
        # func_name = sys._getframe().f_code.co_name    # func  이름
        # print(f'Receive at >>> class : < {cls_name} > function : < {func_name} > !!!')


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
        tabs.addTab(tab1, "Auto Login")
        tabs.addTab(tab2, "2nd Tab")
        tabs.addTab(tab3, "3rd Tab")

        self.setCentralWidget(tabs)
        self.setWindowTitle("AutoTaxTech V1.0 Designed by M.J.Kim ")
        # self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowTitleHint)  # | Qt.FramelessWindowHint)  항상 위에
        # self.setWindowFlags(Qt.FramelessWindowHint)   # windowtitle 제외

        #>>> 메뉴바 https://wikidocs.net/21866  
        # 메뉴바 위젯연결 https://stackoverflow.com/questions/45688873/pyqt5-click-menu-and-open-new-window
        setAction = QAction(QIcon('exit.png'), 'HomeTax Setting', self)
        # setAction.setShortcut('Ctrl+Q')
        # setAction.setStatusTip('HomeTax Setting...')
        setAction.triggered.connect(self.nts_set_clicked)

        exitAction = QAction(QIcon('exit.png'), '종료', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        # self.statusBar()

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('&설정/종료')
        fileMenu.addAction(setAction)
        fileMenu.addAction(exitAction)

        self.setStyleSheet(
                """QMenuBar  { background-color: #7cd3ff; color: blue; font: bold }""")

        # 우하단 위젯
        # rect = QDesktopWidget().screenGeometry()    # 화면해상도   class (0, 0, x, y) 
        rect = QDesktopWidget().availableGeometry()   # 작업표시줄 제외한 화면크기 반환
        max_x = rect.width()
        max_y = rect.height()

        width, height = 380 , 220
        # width, height = 350 , 250
        left = max_x - width 
        top = max_y - height 
        self.setGeometry(left, top, width, height)


    def tab1_layout(self):
        self.le_cta_id = QLineEdit()
        self.le_bs_id = QLineEdit()
        self.le_delay_time = QLineEdit()
        self.btn_nts_login = QPushButton("로그인")
        self.btn_nts_set = QPushButton()
        hbox_nts_btn = QHBoxLayout()
        hbox_nts_btn.addWidget(self.btn_nts_login)
        hbox_nts_btn.addWidget(self.btn_nts_set)
        # QIcon width
        self.btn_nts_set.setIcon(QIcon('data/set.ico'))
        self.btn_nts_set.setFixedWidth(30)

        # 입력제한 http://bitly.kr/wmonM2
        reg_ex = QRegExp("[0-9]+.?[0-9]{,2}")
        input_validator = QRegExpValidator(reg_ex, self.le_delay_time)
        # double_validator = QDoubleValidator(-999.0, 999.0, 2)   ### http://bitly.kr/wmonM2
        self.le_delay_time.setValidator(input_validator)      # double_validator)  
        self.le_delay_time.setMaxLength(3) 
        # 가로 조정
        self.le_cta_id.setFixedWidth(90)

        flo1 = QFormLayout()
        flo1.addRow("CTA No", self.le_cta_id)
        flo1.addRow("부서ID", self.le_bs_id)
        flo1.addRow("delay", self.le_delay_time)
        flo1.addRow(hbox_nts_btn)

        gbox1 = QGroupBox("HomeTax Login")
        # web id pw
        gbox2 = QGroupBox('Website Login')

        flo2 = QFormLayout()
        self.web_gubun_cb = QComboBox()
        # 가로 조정
        self.web_gubun_cb.setFixedWidth(65)
        self.web_cb = QComboBox()
        # self.web_cb.addItems(['Naver','Hanbiro','bizforms','etaxkorea','TheBill'])
        hbox_web_gubun = QHBoxLayout()
        hbox_web_gubun.addWidget(self.web_gubun_cb)
        hbox_web_gubun.addWidget(self.web_cb)

        self.web_id_cb = QComboBox()

        self.web_id_cb.addItems([])

        self.web_id = QLineEdit()
        self.web_pw = QLineEdit()
        hbox_idpw = QHBoxLayout()
        hbox_idpw.addWidget(self.web_id)
        hbox_idpw.addWidget(self.web_pw)

        self.btn_web_login = QPushButton("로그인(save)")
        self.btn_web_set = QPushButton()
        hbox_web_btn = QHBoxLayout()
        hbox_web_btn.addWidget(self.btn_web_login)
        hbox_web_btn.addWidget(self.btn_web_set)
        # QIcon width
        self.btn_web_set.setIcon(QIcon('data/set.ico'))
        self.btn_web_set.setFixedWidth(30)
        # Echomode
        # self.web_pw.setEchoMode(QLineEdit.PasswordEchoOnEdit)  
        # Style
        self.btn_nts_login.setStyleSheet(
                """QPushButton { background-color: #ffff00; color: blue; font: bold }""")       
        self.btn_web_login.setStyleSheet(
                """QPushButton { background-color: #7cd3ff; color: blue; font: bold }""") 
        
        # pyinstaller image err solution
        self.btn_nts_set.setStyleSheet(            
                """QPushButton { border-image: url(:data/set.ico); width:20px; height:20px }""")   # ; width:30px; height:30px           
        self.btn_web_set.setStyleSheet(            
                """QPushButton { border-image: url(:data/set.ico); width:20px; height:20px }""")              

        QToolTip.setFont(QFont('SansSerif', 10))
        self.web_id.setToolTip("<h3>ID 입력</h3>")
        self.web_pw.setToolTip("<h3>Password 입력</h3>")
        self.btn_nts_set.setToolTip("<h3>HomeTax 설정</h3>")
        self.btn_web_set.setToolTip("<h3>Web 설정</h3>")

        flo2.addRow(hbox_web_gubun)
        flo2.addRow("ID select", self.web_id_cb)
        flo2.addRow(hbox_idpw)
        flo2.addRow(hbox_web_btn)

        gbox1.setLayout(flo1)
        gbox2.setLayout(flo2)
        
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

        # mapping text : idpw_list_of_dic
        self.text_map_WebLstDic = {
                            "Naver": web_dict['idpw']['Naver'],
                            "Hanbiro": web_dict['idpw']['Hanbiro'],
                            "nate": web_dict['idpw']['nate'],
                            "daum": web_dict['idpw']['daum'],
                            "gmail": web_dict['idpw']['gmail'],
                            "bizforms": web_dict['idpw']['bizforms'],
                            "etaxkorea": web_dict['idpw']['etaxkorea'],
                            "TheBill": web_dict['idpw']['TheBill']
                            }
        # web Item list
        self.web_gubun_lst = web_dict['gubun']
        self.email_lst = web_dict['email']
        self.website_lst =  web_dict['websites']
        # web combobox additems
        self.web_gubun_cb.addItems(self.web_gubun_lst)
        if self.web_gubun_cb.currentText() == "email":
            self.web_cb.addItems(self.email_lst)
            # Qwidget에 전달할 값 확보
            text = self.web_cb.currentText()
            self.setup_web_widgets(text)

        elif self.web_gubun_cb.currentText() == "websites":
            self.web_cb.addItems(self.website_lst)
            # Qwidget에 전달할 값 확보
            text = self.web_cb.currentText()
            self.setup_web_widgets(text)
        
        # id / pw 추가 입력을 위한 리스트(2)
        self.add_idpw = [None, None]   # [None for i in range(2)]

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
            msg = f"세무법인은 <b>세무사관리번호, 세무사관리번호 비밀번호</b>는 반드시 입력해야 합니다 !!<br>지금 필수사항을 입력하시겠습니까??"
            inst = Util.MsgBoxTF(title, msg)
            TF = inst.initUI()

            if TF==True:
                setting = SettingMenu()
                setting.exec_()
            else:
                pass

        self.set_placeholder() 

        # Nts login Signal connect Slot
        self.le_cta_id.editingFinished.connect(self.cta_id_changed) 
        self.le_bs_id.editingFinished.connect(self.bs_id_changed) 
        self.le_delay_time.editingFinished.connect(self.delay_time_changed) 
        self.btn_nts_login.clicked.connect(self.nts_login_clicked)
        self.btn_nts_set.clicked.connect(self.nts_set_clicked)

        # Web login Signal connect Slot
        self.web_gubun_cb.activated[str].connect(self.on_webgubun_activated)
        self.web_cb.activated[str].connect(self.on_web_activated)
        self.web_id_cb.activated[str].connect(self.on_webid_activated)
        self.web_id.editingFinished.connect(self.web_id_changed)
        self.web_pw.editingFinished.connect(self.web_pw_changed)
        self.btn_web_login.clicked.connect(self.web_login_clicked)
        self.btn_web_set.clicked.connect(self.web_set_clicked)

        self.show()

    def set_placeholder(self):
        self.le_cta_id.setPlaceholderText(nts_dict['secret']['세무사관리번호'])
        self.le_bs_id.setPlaceholderText(nts_dict['secret']['부서아이디'])
        self.le_delay_time.setPlaceholderText(str(nts_dict['secret']['딜레이타임']))

    def cb_id_pw_list(self, idpw_lst_of_dic):
        key_list, idpw_lst = jsconverter.lstOFdic_to_tupKeysVals(idpw_lst_of_dic)
        if idpw_lst == False:   # len(list_of_list) == 0
            _id_lst = ["ID입력요망"] 
            _pw_lst = ["PW입력요망"]
        else:
            _id_lst = [ idpw[0] for idpw in idpw_lst ]
            _pw_lst = [ idpw[1] for idpw in idpw_lst ]

        return (_id_lst, _pw_lst)
    
    def setup_web_widgets(self, text):
        idpw_lst_of_dic = self.text_map_WebLstDic[text]
        id_lst, pw_lst = self.cb_id_pw_list(idpw_lst_of_dic)
        id = id_lst[0]
        pw = pw_lst[0]
        self.web_id.clear()
        self.web_pw.clear()
        self.web_id_cb.clear()
        self.web_id_cb.addItems(id_lst)
        self.web_id.setPlaceholderText(id)
        self.web_pw.setPlaceholderText(pw)


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
            jsconverter.dict_to_json(nts_dict, FULLPATH_NTS_JSON)

    @pyqtSlot()
    def cta_id_changed(self):
        if (self.cta_id != self.le_cta_id.text() and   # value changed
            self.le_cta_id.text() != ""):              # value changed

            text = self.le_cta_id.text()
            self.cta_id = text
            nts_dict['secret']['세무사관리번호'] = text
            # 2. 수정된 딕셔너리를 json 파일로 만들어 저장      
            jsconverter.dict_to_json(nts_dict, FULLPATH_NTS_JSON)
        
    @pyqtSlot()
    def bs_id_changed(self):
        if (self.bs_id != self.le_bs_id.text() and
            self.le_bs_id.text() != ""):

            text = self.le_bs_id.text()
            self.bs_id = text
            nts_dict['secret']['부서아이디'] = text
            # 2. 수정된 딕셔너리를 json 파일로 만들어 저장      
            jsconverter.dict_to_json(nts_dict, FULLPATH_NTS_JSON)

    @pyqtSlot()
    def delay_time_changed(self):
        if (self.delay_time != self.le_delay_time.text() and
            self.le_delay_time.text() !=""):

            text = self.le_delay_time.text()
            self.delay_time = text
            nts_dict['secret']['딜레이타임'] = text
            # 2. 수정된 딕셔너리를 json 파일로 만들어 저장  
            jsconverter.dict_to_json(nts_dict, FULLPATH_NTS_JSON)

    @pyqtSlot()
    def nts_login_clicked(self):
        
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
        
        # 2. 수정된 딕셔너리를 json 파일로 만들어 저장  
        jsconverter.dict_to_json(nts_dict, FULLPATH_NTS_JSON)
        # setplaceholder QLineEdit
        self.set_placeholder()
        # 홈택스 로그인
        login = hometax.Nts_Login()

        login.path2()

    @pyqtSlot()
    def nts_set_clicked(self):       
        widget = SettingMenu()
        self.make_connection(widget)
        widget.exec_()

    # web Slot
    @pyqtSlot(str)
    def on_webgubun_activated(self, text):
        self.web_id.setPlaceholderText("")    
        self.web_pw.setPlaceholderText("")  
        self.web_id_cb.clear()

        if text == "email":
            self.web_cb.clear()
            self.web_cb.addItems(self.email_lst)
            text = self.web_cb.currentText()
            self.setup_web_widgets(text)
        elif text == "websites":
            self.web_cb.clear()
            self.web_cb.addItems(self.website_lst)
            text = self.web_cb.currentText()
            self.setup_web_widgets(text)

        elif text == "banks":
            self.web_cb.clear()
            popup = Util.Errpop()    
            msg = "개발중...<br>comming soon..."
            popup.critical_pop(msg)

    @pyqtSlot(str)
    def on_web_activated(self, text):
        self.add_idpw = [None, None]    # 리스트 초기화 
        self.web_id.setPlaceholderText("")    
        self.web_pw.setPlaceholderText("")    

        self.setup_web_widgets(text)
                
    @pyqtSlot(str)
    def on_webid_activated(self, text): 
        # text == self.web_id_cb.currentText()
        self.web_id.clear()
        self.web_pw.clear()
        self.web_id.setPlaceholderText("")
        self.web_pw.setPlaceholderText("")

        if self.web_cb.currentText() == "Naver":
            self.web_id.setPlaceholderText(text)    
            key_lst, idpw_lst = jsconverter.lstOFdic_to_tupKeysVals(web_dict['idpw']['Naver'])
            for id, pw in idpw_lst:
                if id == text:
                    _pw = pw
                    break
            self.web_pw.setPlaceholderText(_pw)
        elif self.web_cb.currentText() == "Hanbiro":
            self.web_id.setPlaceholderText(text)
            key_lst, idpw_lst = jsconverter.lstOFdic_to_tupKeysVals(web_dict['idpw']['Hanbiro'])
            for id, pw in idpw_lst:
                if id == text:
                    _pw = pw
                    break
            self.web_pw.setPlaceholderText(_pw) 
        elif self.web_cb.currentText() == "bizforms":
            self.web_id.setPlaceholderText(text)
            key_lst, idpw_lst = jsconverter.lstOFdic_to_tupKeysVals(web_dict['idpw']['bizforms'])
            for id, pw in idpw_lst:
                if id == text:
                    _pw = pw
                    break
            self.web_pw.setPlaceholderText(_pw) 
        elif self.web_cb.currentText() == "etaxkorea":
            self.web_id.setPlaceholderText(text)
            key_lst, idpw_lst = jsconverter.lstOFdic_to_tupKeysVals(web_dict['idpw']['etaxkorea'])
            for id, pw in idpw_lst:
                if id == text:
                    _pw = pw
                    break
            self.web_pw.setPlaceholderText(_pw) 
        elif self.web_cb.currentText() == "TheBill":
            self.web_id.setPlaceholderText(text)
            key_lst, idpw_lst = jsconverter.lstOFdic_to_tupKeysVals(web_dict['idpw']['TheBill'])
            for id, pw in idpw_lst:
                if id == text:
                    _pw = pw
                    break
            self.web_pw.setPlaceholderText(_pw)      
        
    @pyqtSlot()
    def web_id_changed(self):       
        temp_id = self.web_id.text()
        self.add_idpw.pop(0)
        self.add_idpw.insert(0, temp_id)
        self.web_id.clear()
        self.web_id.setPlaceholderText("")
        self.web_id.setPlaceholderText(temp_id)

        print("web_id_changed >>",self.add_idpw)

    @pyqtSlot()
    def web_pw_changed(self):       
        temp_pw = self.web_pw.text()
        self.add_idpw.pop(1)
        self.add_idpw.insert(1, temp_pw)
        self.web_pw.clear()
        self.web_pw.setPlaceholderText("")
        self.web_pw.setPlaceholderText(temp_pw)
        print("web_pw_changed >>", self.add_idpw)

    def web_login_pretest(self):
        add_idpw_dic = dict()
        # 1. id / pw placeholderText가 빠진경우
        if (self.web_id.placeholderText() == "ID입력요망" or   
            self.web_id.placeholderText() == "" or
            self.web_pw.placeholderText() == "PW입력요망" or
            self.web_pw.placeholderText() == ""):
            print("1"*10)
            return (False, False)
        # 2. id 입력했는데 pw 입력안한 경우
        elif ((self.add_idpw[0] != ( None or "" )) and
            (self.add_idpw[1] == ( None or "" ))):

            popup = Util.Errpop()    
            msg = "<b>Password</b>를 입력 후 다시 로그인 해주세요!!!) "
            popup.critical_pop(msg)
            print("2"*10)
            return(False, False)
        # 3. pw 만입력 id placeholderText 있는 경우 
        elif ((self.add_idpw[0] == ( None or "" )) and
            (self.web_id.placeholderText() != ("ID입력요망" or "" )) and
            (self.add_idpw[1] != ( None or "" ))):
            new_id = self.web_id.placeholderText()
            new_pw = self.add_idpw[1]
            add_idpw_dic['id'] = new_id
            add_idpw_dic['pw'] = new_pw
            print("3"*10, new_id, new_pw)
            return (True, add_idpw_dic)
        # 4.
        elif (self.add_idpw[0] != None and self.add_idpw[1] != None and
            self.add_idpw[0] != "" and self.add_idpw[1] != ""):     # id / pw 모두 입력
            new_id = self.add_idpw[0]
            new_pw = self.add_idpw[1]
            add_idpw_dic['id'] = new_id
            add_idpw_dic['pw'] = new_pw
            print("4"*10, new_id, new_pw)
            return (True, add_idpw_dic)

        # 5. (id / pw 가 모두 바뀜) or (placeholderText 유효 id,pw 모두 안 바뀜) or (placeholderText 유효한 상황에서 id, pw 중 하나 바뀜)
        elif (self.web_id.placeholderText() != "ID입력요망" and   
            self.web_id.placeholderText() != "" and
            self.web_pw.placeholderText() != "PW입력요망" and
            self.web_pw.placeholderText() != ""):

            new_id = self.web_id.placeholderText()
            new_pw = self.web_pw.placeholderText()
            add_idpw_dic['id'] = new_id
            add_idpw_dic['pw'] = new_pw
            print("5"*10, new_id, new_pw)
            return (True, add_idpw_dic)
        # 6.
        else:
            return (False, False)
        
    @pyqtSlot()
    def web_login_clicked(self):   # >>> web_login_pretest()로 분기
        is_idpw_flag, add_idpw_dic = self.web_login_pretest()
        print("web_login_clicked >>> ", is_idpw_flag, add_idpw_dic)
        if is_idpw_flag==True:
            user_id = add_idpw_dic['id']
            user_pw = add_idpw_dic['pw']

            self.web_id.clear()
            self.web_pw.clear()
            self.web_id.setPlaceholderText(user_id)
            self.web_pw.setPlaceholderText(user_pw)

            select_website_str = self.web_cb.currentText()
            idpw_lst_of_dic = self.text_map_WebLstDic[select_website_str]
            key_lst, idpw_lst = jsconverter.lstOFdic_to_tupKeysVals(idpw_lst_of_dic)
            id_lst, pw_lst = self.cb_id_pw_list(idpw_lst_of_dic)
            # 최초 입력시 빈리스트 인 경우
            if len(idpw_lst_of_dic)==0:
                self.text_map_WebLstDic[select_website_str].insert(0, add_idpw_dic)  # 제일 앞으로
                jsconverter.dict_to_json(web_dict, FULLPATH_WEB_JSON)                # update json file
                self.web_id_cb.clear()
                self.web_id_cb.addItem(user_id)
            else:
                # id 유무 확인하여 pw 만 업데이트
                if user_id in id_lst:       # 동일 id 있으면
                    idx = id_lst.index(user_id)         # index 구하기
                    # pw 일치 확인
                    if user_pw == pw_lst[idx]:           # pw 동일하면 즉시 로그인
                        pop_idpw = idpw_lst.pop(idx)     # json file 순서교체를 위해
                        idpw_lst.insert(0,pop_idpw)      # json file 순서교체를 위해
                        self.text_map_WebLstDic[select_website_str] = jsconverter.lstOFlst_to_lstOFdic(key_lst, idpw_lst)   #######
                        web_dict['idpw'][select_website_str] = self.text_map_WebLstDic[select_website_str]  
                        jsconverter.dict_to_json(web_dict, FULLPATH_WEB_JSON)   # update json file
                        
                    elif user_pw != pw_lst[idx]:         # pw 다르면 업데이트 후 로그인
                        idpw_lst[idx][0] = user_id
                        idpw_lst[idx][1] = user_pw
                        
                        pop_idpw = idpw_lst.pop(idx)     # json file 순서교체를 위해
                        idpw_lst.insert(0, pop_idpw)     # json file 순서교체를 위해
                        self.text_map_WebLstDic[select_website_str] = jsconverter.lstOFlst_to_lstOFdic(key_lst, idpw_lst)   #######
                        web_dict['idpw'][select_website_str] = self.text_map_WebLstDic[select_website_str]  
                        jsconverter.dict_to_json(web_dict, FULLPATH_WEB_JSON)   # update json file

                else:                                        # 동일 id 없으면
                    self.text_map_WebLstDic[select_website_str].insert(0, add_idpw_dic)      # 제일 앞으로
                    jsconverter.dict_to_json(web_dict, FULLPATH_WEB_JSON)   # update json file
                    id_lst.insert(0, user_id)
                    
                    self.web_id_cb.clear()
                    self.web_id_cb.addItems(id_lst)

            if select_website_str == "Naver":
                user_id = self.web_id.placeholderText()
                user_pw = self.web_pw.placeholderText()
                naver = website.NaverMail(user_id, user_pw)
                naver.clipboard_login(naver.ID, naver.PW)

            elif select_website_str == "Hanbiro":
                user_id = self.web_id.placeholderText()
                user_pw = self.web_pw.placeholderText()
                hanbiro = website.Hanbiro(user_id, user_pw)
                hanbiro.login(hanbiro.ID, hanbiro.PW)
            
            elif select_website_str == "nate":
                user_id = self.web_id.placeholderText()
                user_pw = self.web_pw.placeholderText()
                nate = website.Nate(user_id, user_pw)
                nate.login(nate.ID, nate.PW)

            elif select_website_str == "daum":
                user_id = self.web_id.placeholderText()
                user_pw = self.web_pw.placeholderText()
                daum = website.Daum(user_id, user_pw)
                daum.login(daum.ID, daum.PW)

            elif select_website_str == "bizforms":
                user_id = self.web_id.placeholderText()
                user_pw = self.web_pw.placeholderText()
                bizforms = website.Bizforms(user_id, user_pw)
                bizforms.login(bizforms.ID, bizforms.PW)                 

            elif select_website_str == "etaxkorea":
                user_id = self.web_id.placeholderText()
                user_pw = self.web_pw.placeholderText()
                etaxkorea = website.Etaxkorea(user_id, user_pw)
                etaxkorea.login(etaxkorea.ID, etaxkorea.PW) 
            
            elif select_website_str == "TheBill":
                user_id = self.web_id.placeholderText()
                user_pw = self.web_pw.placeholderText()
                theBill = website.TheBill(user_id, user_pw)
                theBill.login(theBill.ID, theBill.PW)

            # combobox 순서 변경
            select_web_gubun = self.web_gubun_cb.currentText()
            select_web_gubun_idx = web_dict['gubun'].index(select_web_gubun)
            pop_web_gubun = web_dict['gubun'].pop(select_web_gubun_idx)
            web_dict['gubun'].insert(0, pop_web_gubun) 

            select_web_site = self.web_cb.currentText()
            if select_web_site in web_dict['email']:
                select_web_site_idx = web_dict['email'].index(select_web_site)
                pop_web_site = web_dict['email'].pop(select_web_site_idx)
                web_dict['email'].insert(0, pop_web_site)
            elif select_web_site in web_dict['websites']:
                select_web_site_idx = web_dict['websites'].index(select_web_site)
                pop_web_site = web_dict['websites'].pop(select_web_site_idx)
                web_dict['websites'].insert(0, pop_web_site)

            jsconverter.dict_to_json(web_dict, FULLPATH_WEB_JSON)   # update json file
            ##
        else:
            popup = Util.Errpop()    
            msg = "<b>ID / PW</b>를 선택(입력)후 다시 로그인 해주세요!!!) "
            popup.critical_pop(msg)         
                    
    @pyqtSlot()
    def web_set_clicked(self):       
        popup = Util.Errpop()    
        msg = "개발중...<br>comming soon..."
        popup.critical_pop(msg)

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
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())
        
