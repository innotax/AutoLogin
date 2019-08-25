from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

''' https://freeprog.tistory.com/351
'''

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

class Test:
    def __init__(self):
        name = ""

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
        self.th.sec_changed.connect(self.time_update)

        self.add_sec_signal.connect(self.th.add_sec)
        self.send_instance_signal.connect(self.th.recive_instance_signal)
        self.show()

    @pyqtSlot()
    def time_start(self):
        self.th.start()
        self.th.working = True

    @pyqtSlot()
    def time_stop(self):
        self.th.working = False

    @pyqtSlot()
    def add_sec(self):
        print(".... add signal emit ....")
        self.add_sec_signal.emit()

    @pyqtSlot(str)
    def time_update(self, msg):
        self.qtxt1.append(msg)

    @pyqtSlot()
    def send_instance(self):
        t1 = Test()
        t1.name = "SuperPower!!!"
        self.send_instance_signal.emit(t1)
        

class Worker(QThread):
    sec_changed = pyqtSignal(str)

    def __init__(self, sec=0, parent=None):
        super().__init__()
        self.main = parent
        self.working = True
        self.sec = sec

    def __del__(self):
        print('end thread.....')
        self.wait()

    def run(self):
        while self.working:
            self.sec_changed.emit('time (secs) : {}'.format(self.sec))
            self.sleep(1)
            self.sec += 1

    @pyqtSlot()
    def add_sec(self):
        print('add sec...')
        self.sec += 100

    @pyqtSlot("PyQt_PyObject")
    def recive_instance_signal(self, inst):
        print(inst.name)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = MyMain()
    app.exec_()
        
        
        
        
