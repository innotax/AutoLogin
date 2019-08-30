import os, sys, json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDesktopWidget, QWidget, QDialog, 
                            QPushButton, QRadioButton, QLabel, QLineEdit, QAction, QToolTip, qApp)
from PyQt5.QtWidgets import QMessageBox, QTabWidget, QGridLayout, QGroupBox, QHBoxLayout, QVBoxLayout, QFormLayout
from PyQt5.QtGui import QIcon, QRegExpValidator, QDoubleValidator, QIntValidator, QFont
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QRegExp

full_js_fn  = os.path.join(os.path.dirname(__file__), "test.json")
# p = os.path.dirname(__file__)
# print(p)
print(full_js_fn)

with open(full_js_fn, 'r', encoding='utf-8') as fn:
    js_dic =  json.load(fn)

print(type(js_dic), js_dic, id(js_dic))

class UI_D1(QDialog):
    changed_le1 = pyqtSignal(str)
    def __init__(self, parent=None):
        super(UI_D1, self).__init__()

        self.initUI()

    def initUI(self):
        self.le1 = QLineEdit()
        le2 = QLineEdit()
        btn = QPushButton("Save")

        flo = QFormLayout()
        flo.addRow("Delay", self.le1)
        flo.addRow("BsId", le2)        
        flo.addRow(btn)        

        self.setLayout(flo)

        self.le1.setPlaceholderText(js_dic['delay'])
        le2.setPlaceholderText(js_dic['bsid'])

        self.le1.editingFinished.connect(self.leChanged)
        le2.textChanged.connect(self.leChanged)
        # le2.textChanged.connect(UI_D1.s_d1)

    def leChanged(self):
        # print(self)
        txt = self.le1.text()
        js_dic['delay'] = txt
        print(txt)
        self.changed_le1.emit(txt)
        print("*"*10)
    
    def make_connection(self, main_object):
        print("="*3)
        main_object.changed_le1.connect(self.on_receive_signal)

    @pyqtSlot(str)
    def on_receive_signal(self, val):
        self.le1.setText(val)
        self.le1.setPlaceholderText(val)

        cls_name = self.__class__.__name__            # class 이름
        func_name = sys._getframe().f_code.co_name    # func  이름
        print(f'Receive at >>> class : < {cls_name} > function : < {func_name} > !!!')
        # print('from {} receive'.format(self.__class__.__name__))
        print(val)


    # self.show()

class UI_Main(QMainWindow):
    # changed_le1 = pyqtSignal(str)   # 1. Signal 객체를 담을 inst 생성
    def __init__(self):
        super(UI_Main, self).__init__()

        self.initUI()

    def initUI(self):
   
        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()
        tab4 = QWidget()

        self.le1 = QLineEdit()
        le2 = QLineEdit()
        le3 = QLineEdit()
        self.btn = QPushButton("Save")

        flo = QFormLayout()
        flo.addRow("Delay", self.le1)
        flo.addRow("BsId", le2)
        flo.addRow("CtaId", le3)
        flo.addRow(self.btn) 

        gbox = QGroupBox("gbox1")
        gbox2 = QGroupBox("gbox2")

        gbox.setLayout(flo)

        hbox = QHBoxLayout()
        hbox.addWidget(gbox)
        hbox.addWidget(gbox2)

        tab1.setLayout(hbox) 

        tabs = QTabWidget()
        tabs.addTab(tab1, '1st')
        tabs.addTab(tab2, '2nd')
        tabs.addTab(tab3, '3rd')
        tabs.addTab(tab4, '4th')

        self.setCentralWidget(tabs)

        self.le1.setPlaceholderText(js_dic['delay'])
        le2.setPlaceholderText(js_dic['bsid'])
        le3.setPlaceholderText(js_dic['CtaId'])

        setAction = QAction(QIcon('exit.png'), 'Setting', self)
        setAction.triggered.connect(self.setting)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('&메뉴')
        fileMenu.addAction(setAction)

        print('1'*10,self.le1.text())
        print('2'*10,self.le1.placeholderText())
        self.le1.setText(self.le1.placeholderText())
        print('3'*10,self.le1.text())


        self.show()

    
    def setting(self):
        print('setAction')
        d1 = UI_D1()
        self.make_connection(d1)
        d1.exec_()

class Main(UI_Main):
    changed_le1 = pyqtSignal(str)   # 1. Signal 객체를 담을 inst 생성
    def __init__(self, parent=None):
        super(Main, self).__init__( )

        setAction = QAction(QIcon('exit.png'), 'Setting', self)
        setAction.triggered.connect(self.setting)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('&메뉴')
        fileMenu.addAction(setAction)

        self.le1.editingFinished.connect(self.leChanged)
        self.btn.clicked.connect(self.btn_clicked)

        self.show()
    
    def make_connection(self, d1_object):
        print("="*3)
        d1_object.changed_le1.connect(self.receive_d1)

    def leChanged(self):
        # print(self)
        txt = self.le1.text()
        js_dic['delay'] = txt
        
        self.changed_le1.emit(txt)
        print("2"*10)
        print(self.le1.editingFinished.__class__.__name__)
        if isinstance(self.le1.editingFinished ,pyqtSignal):
            print('isinstance')  
        if self.le1.editingFinished.__class__.__name__ == 'pyqtBoundSignal':
            print('clsname')
        if self.le1.editingFinished != True:
            print(self.le1.editingFinished)
        print("2"*50)
    def btn_clicked(self):
        txt = self.le1.text()
        self.changed_le1.emit(txt) 
    
    @pyqtSlot(str)
    def receive_d1(self,val):
        self.le1.setText(val)
        self.le1.setPlaceholderText(val)

        cls_name = self.__class__.__name__            # class 이름
        func_name = sys._getframe().f_code.co_name    # func  이름
        print(f'Receive at >>> class : < {cls_name} > function : < {func_name} > !!!')
        # print('from {} receive'.format(self.__class__.__name__))
        print(val)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dia = UI_D1()
    main = Main()
    # main.make_connection(dia)
    dia.make_connection(main)
    sys.exit(app.exec_())

