import sys, json
# import pandas as pd
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QTableWidget,QTableWidgetItem,QVBoxLayout,
                            QCheckBox, QPushButton, QComboBox)
from PyQt5 import Qt,QtCore

class TableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Checkbox in Table'
        self.left = 0
        self.top = 0
        self.width = 640
        self.height = 480        
        self.numRow = 5
        self.numCol = 5

        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)        
        self.createTable()               
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget) 
        self.btn = QPushButton("save")
        self.layout.addWidget(self.btn)
        self.setLayout(self.layout) 

        # Show widget
        self.show()
     

    def createTable(self):       
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(self.numRow)        
        self.tableWidget.setColumnCount(self.numCol)                
        self.tableWidget.move(0,0)        

        self.InsertTable()
   

    def InsertTable(self):                        
        self.checkBoxList = []
        for i in range(self.numRow):
            ckbox = QCheckBox()
            self.checkBoxList.append(ckbox)

        for i in range(self.numRow):                          
            self.tableWidget.setCellWidget(i,0,self.checkBoxList[i]) 

        # self.comboBoxList = []
        # for i in range(self.numRow):
        #     cbbox = QComboBox()
        #     self.comboBoxList.append(cbbox)

        # for i in range(self.numRow):                          
        #     self.tableWidget.setCellWidget(i,1,self.comboBoxList[i])                                    
        
        # self.tableWidget.move(0,0)                 

 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TableWidget()
    sys.exit(app.exec_())  