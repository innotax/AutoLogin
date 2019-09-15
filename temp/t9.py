import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from pandas import DataFrame
import sys, json
 
""" QTableWidget       : http://bitly.kr/cyM01Yn
    widget 창에 꽉 차게 : http://bitly.kr/l8mzD7J
    Add checkbox in QTableView header using icons :  https://tinyurl.com/y53kuh3n
    QTableWidget 고급예제 : https://freeprog.tistory.com/352
"""
 
# data_single = {'hi': ['a', 'b'], 'hi2': ['d', 'c']}
tell_row=1

#============== 1. json to dic
fulljs = r'C:\Ataxtech\ATT\Ver1.0\json\web.json'

with open(fulljs, encoding='utf-8') as fn:
    dic = json.load(fn)                      # dic : dic_dic_lst_dic
idpw_dic_lst_dic = dic['idpw']               # idpw_dic_lst_dic : dic_lst_dic

print("  1. >> type(idpw_dic_lst_dic) : ", type(idpw_dic_lst_dic), "="*100)

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
            
# data_single = pd.DataFrame(web_id_pw, columns=columns) 
data_single = web_id_pw

class TableWidget(QTableWidget):
    def __init__(self, df, parent=None):
        QTableWidget.__init__(self, parent)
        self.df = df
        nRows = len(self.df.index)
        nColumns = len(self.df.columns)
        self.setRowCount(nRows)
        self.setColumnCount(nColumns)
 
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                x = self.df.iloc[row, col]
                self.setItem(row, col, QTableWidgetItem(x))

        # Add checkbox : http://bitly.kr/30NASEh 
        self.checkbox_col = nColumns + 1                 # checkbox 핸들링 위해
        self.setColumnCount(self.checkbox_col)
        for row in range(self.rowCount()):            
            checkbox = QTableWidgetItem()
            checkbox.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkbox.setCheckState(Qt.Unchecked)       
            self.setItem(row, nColumns, checkbox)
 
        self.cellChanged.connect(self.onCellChanged)
 
    #@pyqtSlot(int, int)
    def onCellChanged(self, row, column):
        sender_obj = self.sender()
        print("   >>>sender_obj ",sender_obj)
        if column == self.checkbox_col-1:          # checkbox checked
            idx_row = row
            print(idx_row)

        text = self.item(row, column).text()
        # number = float(text)
        print(row, column, text)
        self.df.set_value(row, column, text)
 
 
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        # self.setGeometry(700, 100, 350, 380)
        # df_rows = tell_row
        # df_cols = 1
        df = pd.DataFrame(data_single, columns=columns)
        self.tableWidget = TableWidget(df, self)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

        # widget 창에 꽉 차게 http://bitly.kr/l8mzD7J
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # =====
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.button = QPushButton('Print DataFrame', self)
        self.layout.addWidget(self.button)
        
        self.setLayout(self.layout)
        self.button.clicked.connect(self.print_my_df)
 
    @pyqtSlot()
    def print_my_df(self):
        some_df =self.tableWidget.df
        print(some_df)
 
        fn, _ = QFileDialog.getSaveFileName(self, 'Speichern unter', None, 'Excel Dateien (.xlsx);;Alle Dateien()')
        if fn != '':
            if QFileInfo(fn).suffix() == "": fn += '.xlsx'
        df = DataFrame(some_df)
        df.to_excel(fn, sheet_name='Ergebnisse', index=False)
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())