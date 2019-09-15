import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *

""" http://bitly.kr/l8mzD7J
"""

class Table(QWidget):
    def __init__(self, arg=None):
        super(Table, self).__init__(arg)
        self.setWindowTitle("QTableView")       

        self.model = QStandardItemModel(4, 4);
        self.model.setHorizontalHeaderLabels(['Heading 1','Heading 2','Heading 3','Heading 4'])

        for row in range(4):
            for column in range(4):
                item = QStandardItem("row {}, column {}  {} ".format(row, column, "*** "*column))
                self.model.setItem(row, column, item)

        self.tableView = QTableView()
        self.tableView.setModel(self.model)

        # +++
        self.tableView.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        dlgLayout = QVBoxLayout();
        dlgLayout.addWidget(self.tableView)
        self.setLayout(dlgLayout)

if __name__ == '__main__':
    app   = QApplication(sys.argv)  
    table = Table()
    table.show()
    sys.exit(app.exec_())