from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class MyMainGUI(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.qtxt1 = QTextEdit(self)
        self.btn1 = QPushButton("Start", self)
        self.btn2 = QPushButton("Stop", self)
        self.btn3 = QPushButton("add 100", self)
        self.btn4 = QPushButton("send instance", self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.qtxt1)
        vbox.addWidget(self.btn1)
        vbox.addWidget(self.btn2)
        vbox.addWidget(self.btn3)
        vbox.addWidget(self.btn4)
        self.setLayout(vbox)

        self.setGeometry(100,50,300,300)

        # self.show()

class MyMain(MyMainGUI):
    add_sec_signal = pyqtSignal()
    send_instance_signal = pyqtSignal("PyQt_PyObject")

    def __init__(self, parent=None):
        super().__init__(parent)

        self.btn1.clicked.connect(self.time_start)
        self.btn2.clicked.connect(self.time_stop)
        self.btn3.clicked.connect(self.add_sec)
        self.btn4.clicked.connect(self.send_instance)

        self.th = Worker(parent=self)

    @pyqtSlot()
    def time_start(self):
        pass

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = MyMainGUI()
    app.exec_()
        
        
        
        
