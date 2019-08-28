import sys
from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import (QWidget, QLCDNumber, QSlider,
    QVBoxLayout, QApplication)
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QRegExp


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def printLabel(self, str):
        print('printLabel:',str)

    def initUI(self):

        lcd = QLCDNumber(self)
        sld = QSlider(Qt.Horizontal, self)

        vbox = QVBoxLayout()
        vbox.addWidget(lcd)
        vbox.addWidget(sld)

        self.setLayout(vbox)

        #This line works
        sld.valueChanged.connect(lcd.display)

        #connect to a user-defined lot
        sld.valueChanged.connect(self.printLabel)

        #any python callable will do
        # sld.valueChanged.connect(lambda x: print('lambda:', x))
        sld.valueChanged.connect(lambda x: self.pp(x))

        #This line does not work
        #sld.valueChanged.connect(lcd.display, self.printLabel("hi"))

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Signal & slot')
        self.show()

    # @pyqtSlot(int)
    def pp(self, y):
        print('lambda : ', y)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())