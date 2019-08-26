import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class testUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        le1 = QLineEdit()
        le2 = QLineEdit()
        le3 = QLineEdit()

        flo1 = QFormLayout()
        flo1.addRow('에디터 1', le1)
        flo1.addRow('에디터 2', le2)
        flo1.addRow('에디터 3', le3)

        le11 = QLineEdit()
        le21 = QLineEdit()
        le31 = QLineEdit()
        btn = QPushButton("save")
        btn1 = QPushButton("cancel")
        h = QHBoxLayout()
        h.addWidget(btn)
        h.addWidget(btn1)

        flo2 = QFormLayout()
        flo2.addRow('에디터 1', le11)
        flo2.addRow('에디터 2', le21)
        flo2.addRow('에디터 3', le31)
        flo2.addRow(h)

        hbox = QHBoxLayout()
        # hbox = QVBoxLayout()
        hbox.addLayout(flo1)
        hbox.addLayout(flo2)
        # hbox.addWidget(flo1)
        # hbox.addWidget(flo2)

        self.setLayout(hbox)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    te = testUI()
    app.exec_()


