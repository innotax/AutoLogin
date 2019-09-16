import sys, json
from pprint import pprint
import numpy
import pandas as pd
# from PyQt5.QtWidgets import QApplication, QTableView, QTableWidget, QWidget
# from PyQt5.QtCore import QAbstractTableModel, Qt 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
# from PyQt5 import QtCore

# df = pd.DataFrame({'a': ['Mary', 'Jim', 'John'],
#                    'b': [100, 200, 300],
#                    'c': ['a', 'b', 'c']})

#============== 1. json to dic
fulljs = r'C:\Ataxtech\ATT\Ver1.0\json\web.json'

with open(fulljs, encoding='utf-8') as fn:
    dic = json.load(fn)                      # dic : dic_dic_lst_dic
idpw_dic_lst_dic = dic['idpw']               # idpw_dic_lst_dic : dic_lst_dic

print("  1. >> type(idpw_dic_lst_dic) : ", type(idpw_dic_lst_dic), "="*100)
pprint(idpw_dic_lst_dic)

#============== 2. dic_lst_dic to Dataframe
columns = ['website', 'id', 'pw']      # website : dic_lst_dic.keys() 컬럼
web_id_pw = []
for website in idpw_dic_lst_dic.keys():    
    idpw_lst_dic = idpw_dic_lst_dic[website]
    if idpw_lst_dic:
        for d in idpw_lst_dic:
            _id = d['id']
            _pw = d['pw']
            web_id_pw.append([website, _id, _pw])
            continue
        continue
    web_id_pw.append([website, "", ""])        # id,pw 없는 사이트 관리 위해
            
df = pd.DataFrame(web_id_pw, columns=columns)


class PandasModel(QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """

    def __init__(self, data, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return self._data.index[col]
        return None
    # ======= editable cell 수정 # https://stackoverflow.com/questions/38020127/make-qtableview-column-read-only-using-python
    def flags(self, index):
        flag = super(self.__class__,self).flags(index)
        if  (index.column() == 0):
            # return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
            # flag |= Qt.ItemIsEditable    # read-only
            flag |= Qt.ItemIsSelectable
            flag |= Qt.ItemIsEnabled
            flag |= Qt.ItemIsDragEnabled
            flag |= Qt.ItemIsDropEnabled
        else:
            # return Qt.ItemIsEnabled | Qt.ItemIsSelectable                                        
            flag |= Qt.ItemIsEditable
            flag |= Qt.ItemIsSelectable
            flag |= Qt.ItemIsEnabled
            flag |= Qt.ItemIsDragEnabled
            flag |= Qt.ItemIsDropEnabled
        return flag
    
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid():
            row = index.row()
            col = index.column()
            self._data.iloc[row][col] = str(value)  #   float(value)
            self.dataChanged.emit(index, index, (Qt.DisplayRole, ))
            return True
        return False
    ### ======= editable cell

class AddTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__( parent)
        
        # self.table = QTableWidget(parent)
        # self._mainwin = parent
        self.setColumnCount(3)
        self.setRowCount(1)

        header_labels = ['Website', 'ID', 'PW']
        self.setHorizontalHeaderLabels(header_labels)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # header color : https://stackoverflow.com/questions/19198634/pyqt-qtablewidget-horizontalheaderlabel-stylesheet
        stylesheet = """QHeaderView::section{ background-color: #7cd3ff; color: blue;  }"""
        self.horizontalHeader().setStyleSheet(stylesheet)

        web_cb = QComboBox()
        items = list(idpw_dic_lst_dic.keys())
        web_cb.addItems(items)

        self.setCellWidget(0, 0, web_cb)


        # self.setItem(0, 0, QTableWidgetItem(""))
        # self.setItem(0, 1, QTableWidgetItem(""))
        # self.setItem(0, 2, QTableWidgetItem(""))


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.df = df
        model = PandasModel(self.df)
        self.view = QTableView()
        self.view.setModel(model)

        # widget 창에 꽉 차게 http://bitly.kr/l8mzD7J
        self.view.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # =====
        # header color : https://stackoverflow.com/questions/19198634/pyqt-qtablewidget-horizontalheaderlabel-stylesheet
        stylesheet = """QHeaderView::section{ background-color: #7cd3ff; color: blue;  }"""
        self.view.horizontalHeader().setStyleSheet(stylesheet)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.view)
        self.btn1 = QPushButton('Save DataFrame', self)
        self.btn2 = QPushButton('Add Row', self)
        self.layout.addWidget(self.btn1)
        self.layout.addWidget(self.btn2)
        self.add_table = AddTable(self)
        self.add_table.setHidden(True)
        self.layout.addWidget(self.add_table)

        self.setLayout(self.layout)
        self.btn1.clicked.connect(self.print_my_df)
        self.btn2.clicked.connect(self.add_row)
 
    @pyqtSlot()
    def print_my_df(self):
        # some_df =self.tableWidget.df
        some_df =self.df
        print(some_df)
 
        fn, _ = QFileDialog.getSaveFileName(self, 'Speichern unter', None, 'Excel Dateien (.xlsx);;Alle Dateien()')
        if fn != '':
            if QFileInfo(fn).suffix() == "": 
                fn += '.xlsx'
        else:
            fn = "nameless"
            if QFileInfo(fn).suffix() == "": 
                fn += '.xlsx'
            
        self.df = pd.DataFrame(some_df)
        self.df.to_excel(fn, sheet_name='Ergebnisse', index=False)
    
    @pyqtSlot()
    def add_row(self):
        sender_obj = self.sender()
        print(sender_obj, sender_obj.text())
        if sender_obj.text() == "Add Row":
            self.add_table.setHidden(False)
            self.layout.addWidget(self.add_table)
            self.setLayout(self.layout)
            sender_obj.setText("Del Row")
        elif sender_obj.text() == "Del Row":
            self.add_table.setHidden(True)
            # self.layout.removeWidget(sender_obj)
            # self.layout.removeWidget(self.btn3)
            # sender_obj.deleteLater()
            self.setLayout(self.layout)
            sender_obj.setText("Add Row")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    # model = PandasModel(df)
    # # view = QTableWidget()
    # view = QTableView()
    # view.setModel(model)
    # # view.resize(800, 600)
    # view.show()
    sys.exit(app.exec_())