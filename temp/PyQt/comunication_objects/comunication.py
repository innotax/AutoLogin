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
        print(txt)
        self.changed_le1.emit(txt)
        print("*"*10)

    # self.show()

class UI_Main(QMainWindow):
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
        btn = QPushButton("Save")

        flo = QFormLayout()
        flo.addRow("Delay", self.le1)
        flo.addRow("BsId", le2)
        flo.addRow("CtaId", le3)
        flo.addRow(btn) 

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

        self.show()
    
    # def make_connection(self, d1_object):
    #     print("="*3)
    #     d1_object.changed_le1.connect(self.receive_d1)
    
    # @pyqtSlot(str)
    # def receive_d1(self,val):
        
    #     print('receive')
    #     self.le1.setPlaceholderText(val)
    #     print(val)

    
    def setting(self):
        print('setAction')
        d1 = UI_D1()
        self.make_connection(d1)
        d1.exec_()

class Main(UI_Main):
    def __init__(self, parent=None):
        super(Main, self).__init__( )

        setAction = QAction(QIcon('exit.png'), 'Setting', self)
        setAction.triggered.connect(self.setting)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('&메뉴')
        fileMenu.addAction(setAction)

        self.show()
    
    def make_connection(self, d1_object):
        print("="*3)
        d1_object.changed_le1.connect(self.receive_d1)
    
    @pyqtSlot(str)
    def receive_d1(self,val):
        self.le1.setPlaceholderText(val)
        print('receive')
        print(val)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dia = UI_D1()
    main = Main()
    main.make_connection(dia)
    sys.exit(app.exec_())

