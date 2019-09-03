'''
import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt

df = pd.DataFrame({'a': ['Mary', 'Jim', 'John'],
                   'b': [100, 200, 300],
                   'c': ['a', 'b', 'c']})

class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = pandasModel(df)
    view = QTableView()
    view.setModel(model)
    view.resize(800, 600)
    view.show()
    sys.exit(app.exec_())
'''
'''
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import random

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt rectangle colors - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 440
        self.height = 280
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        # Set window background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
        
        # Add paint widget and paint
        self.m = PaintWidget(self)
        self.m.move(0,0)
        self.m.resize(self.width,self.height)
        
        self.show()
    
class PaintWidget(QWidget):
    def paintEvent(self, event):
        qp = QPainter(self)
        
        qp.setPen(Qt.black)
        size = self.size()
        
        # Colored rectangles
        qp.setBrush(QColor(200, 0, 0))
        qp.drawRect(0, 0, 100, 100)
        
        qp.setBrush(QColor(0, 200, 0))
        qp.drawRect(100, 0, 100, 100)
        
        qp.setBrush(QColor(0, 0, 200))
        qp.drawRect(200, 0, 100, 100)
        
        # Color Effect
        for i in range(0,100):
            qp.setBrush(QColor(i*10, 0, 0))
            qp.drawRect(10*i, 100, 10, 32)
            
            qp.setBrush(QColor(i*10, i*10, 0))
            qp.drawRect(10*i, 100+32, 10, 32)
            
            qp.setBrush(QColor(i*2, i*10, i*1))
            qp.drawRect(10*i, 100+64, 10, 32)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
'''
from PyQt5 import sim