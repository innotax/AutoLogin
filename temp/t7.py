from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import random

class MyTable(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.table = QTableWidget(parent)
        self._mainwin = parent

        self.__make_layout()
        self.__make_table()
    
    def __make_table(self):
        self.table.setSelectionBehavior(QTableView.SelectRows)
        # self.table.setSelectionMode(QAbstractItemView.SingleSelection)

        self.table.setColumnCount(5)
        self.table.setRowCount(10)
        self.table.setHorizontalHeaderLabels(["코드", "종목명"])
        header_item = QTableWidgetItem("추가")
        header_item.setBackground(Qt.red)  # 헤더 배경색 설정 --> app.setStyle() 설정해야만 작동한다.
        self.table.setHorizontalHeaderItem(2, header_item)


        
        

    def __make_layout(self):
        vox = QVBoxLayout()
        

        # grid = QGridLayout()
        # vox.addLayout(grid)
        vox.addWidget(self.table)
        hbox = QHBoxLayout()
        flo = QFormLayout()
        btn1 = QPushButton("All Del")
        btn2 = QPushButton("All save")
        hbox.addWidget(btn1)
        hbox.addWidget(btn2)
        flo.addRow("삭제 추가 저장", hbox)
        vox.addLayout(flo)
        self.setLayout(vox)

        

        
        # grid.addWidget(btn1, 0, 1)
        
        # grid.addWidget(btn2, 0, 2)

        

class MyMain(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        table = MyTable()

        self.setCentralWidget(table)
        self.statusbar = self.statusBar()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))

    w = MyMain()
    w.show()
    sys.exit(app.exec())
