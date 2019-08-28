from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
    QSizePolicy, QLabel, QFontDialog, QApplication)
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QRegExp
import sys

class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):      

        vbox = QVBoxLayout()

        btn = QPushButton('Dialog', self)
        btn.setSizePolicy(QSizePolicy.Fixed,
            QSizePolicy.Fixed)
        
        btn.move(20, 20)

        vbox.addWidget(btn)

        connect_funcs = [self.showDialog, self.f1, self.f2, self.f3]
        btn.clicked.connect(lambda x: x for x in connect_funcs)
        
        self.lbl = QLabel('Knowledge only matters', self)
        self.lbl.move(130, 20)

        vbox.addWidget(self.lbl)
        self.setLayout(vbox)          
        
        self.setGeometry(300, 300, 250, 180)
        self.setWindowTitle('Font dialog')
        self.show()
        
        
    def showDialog(self):

        font, ok = QFontDialog.getFont()
        print(font,ok)
        if ok:
            self.lbl.setFont(font)
    
    @pyqtSlot()
    def f1(): 
        print('*'*10)
    
    @pyqtSlot()
    def f2(): 
        print('#'*20)
    
    @pyqtSlot()
    def f3(): 
        print('!'*30)

        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())