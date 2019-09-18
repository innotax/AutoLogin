import os, sys, json
from pprint import pprint
# import numpy
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QWidget, QTableView, QTableWidget, QTableWidgetItem, 
                        QAbstractItemView, QAbstractScrollArea, QHeaderView, QSizePolicy, QAction,
                        QVBoxLayout, QPushButton, QComboBox, QLabel, QLineEdit, QDesktopWidget)
from PyQt5.QtCore import QAbstractTableModel, Qt, pyqtSignal, pyqtSlot 

# 상위폴더 내 파일 import  https://brownbears.tistory.com/296
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))   

import atmui

""" QTableWidget       : http://bitly.kr/cyM01Yn  엑셀저장
    widget 창에 꽉 차게 : http://bitly.kr/l8mzD7J
    Add checkbox in QTableView header using icons :  https://tinyurl.com/y53kuh3n
    QTableWidget 고급예제 : https://freeprog.tistory.com/352
    read-only : http://bitly.kr/Fa7Q45v
    공학자를 위한 PySide2      https://wikidocs.net/36797
    https://freeprog.tistory.com/334 [취미로 하는 프로그래밍 !!!]
    Qt Style Sheets Examples : https://hoy.kr/d0nYi
"""
fulljs = r'C:\Ataxtech\ATT\Ver1.0\json\web.json'

def ddld_json_to_df(fulljs = r'C:\Ataxtech\ATT\Ver1.0\json\web.json'):
    #============== 1. json to ddld_dic
    with open(fulljs, encoding='utf-8') as fn:
        ddld_dic = json.load(fn)                      # ddld_dic : dic_dic_lst_dic
    idpw_dic_lst_dic = ddld_dic['idpw']               # idpw_dic_lst_dic : dic_lst_dic

    #============== 2. dic_lst_dic to Dataframe
    columns = ['website', 'id', 'pw']      # website : dic_lst_dic.keys() 컬럼
    web_id_pw = []
    empty_site_lst = []                             # id,pw 없는 사이트 json file 관리 위해 2
    for website in idpw_dic_lst_dic.keys():    
        idpw_lst_dic = idpw_dic_lst_dic[website]
        if idpw_lst_dic:
            for d in idpw_lst_dic:
                _id = d['id']
                _pw = d['pw']
                web_id_pw.append([website, _id, _pw])
                continue
            continue
        # web_id_pw.append([website, "", ""])        # id,pw 없는 사이트 관리 위해 1
        empty_site_lst.append(website)               # id,pw 없는 사이트 json file 관리 위해 2
                
    df = pd.DataFrame(web_id_pw, columns=columns)

    return ddld_dic, idpw_dic_lst_dic, df


class PandasModel(QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """
    # 1. Signal 객체를 담을 inst 생성
    view_edit_signal = pyqtSignal()

    def __init__(self, data=None, parent=None):
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
            # 2. 시그널 객체 방출
            self.view_edit_signal.emit()
            return True
        return False
    ### ======= editable cell
    # # enable sorting : https://codeday.me/ko/qa/20190422/381866.html
    # # 삭제시 df 와 tablevew 간의 row index 일치시키기 위해 죽여놓음
    # def sort(self, Ncol, order):
    #     """Sort table by given column number.
    #     """
    #     try:
    #         self.layoutAboutToBeChanged.emit()
    #         self._data = self._data.sort_values(self._data.columns[Ncol], ascending=not order)
    #         self.layoutChanged.emit()
    #     except Exception as e:
    #         print(e)

class AddTable(QTableWidget):
    """ https://freeprog.tistory.com/333
    """
    ddld_dic, idpw_dic_lst_dic, df = ddld_json_to_df()
    item_set = set(idpw_dic_lst_dic.keys())
    # 1. Signal 객체를 담을 inst 생성
    pw_changed_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.website = ""
        self.id = ""
        self.pw = ""
        
        self.setColumnCount(3)
        self.setRowCount(1)

        header_labels = ['Website', 'ID', 'PW']
        self.setHorizontalHeaderLabels(header_labels)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # header color : https://stackoverflow.com/questions/19198634/pyqt-qtablewidget-horizontalheaderlabel-stylesheet
        stylesheet = """QHeaderView::section{ background-color: #7cd3ff; color: blue;  }"""
        self.horizontalHeader().setStyleSheet(stylesheet)

        # 콤보박스 https://freeprog.tistory.com/333
        web_cb = QComboBox()
        # items = list(set(idpw_dic_lst_dic.keys()))
        web_cb.addItems(list(self.item_set))
        self.setCellWidget(0, 0, web_cb)

        self.website = web_cb.currentText()
        # print(' 1>>> ',self.website,'===', self.id, '===', self.pw)

        web_cb.currentTextChanged.connect(self.cbTextChanged)   
        self.cellChanged.connect(self.onCellChanged)
    
    def cbTextChanged(self, txt):
        self.website = txt

    def onCellChanged(self, row, col):
        if col == 1:
            self.id = self.item(0, 1).text()
            # 2. 시그널 객체 방출
            self.pw_changed_signal.emit()
        elif col == 2:
            self.pw = self.item(0, 2).text()
            # 2. 시그널 객체 방출
            self.pw_changed_signal.emit()
    
    
class Ui_WebSetting(QWidget):
    # 1. Signal obj
    json_update_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("Web ID/PW 관리")
        # 우하단 위젯   # self.setGeometry(300,300,500,10)
        rect = QDesktopWidget().availableGeometry()   # 작업표시줄 제외한 화면크기 반환 # .screenGeometry() : 화면해상도 class (0, 0, x, y)
        max_x = rect.width()
        max_y = rect.height()

        width, height = 300 , 300
        left = max_x - width 
        top = max_y - height 

        self.setGeometry(left, top-500, width, height)

        result = ddld_json_to_df()
        self.ddld_dic = result[0]
        self.idpw_dic_lst_dic = result[1]
        self._df = result[2]   
        
        self.initUI()
        # self.show()

    def initUI(self):
        
        self.df = self._df
        self.emty_site_set = AddTable.item_set - set(self.df['website'].to_list())

        self.model = PandasModel(self.df)
        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.setSelectionBehavior(QTableView.SelectRows)  # multiple row 단위 선택 가능
        # self.view.setSelectionMode(QTableView.SingleSelection)  # one row 선택 제한
        self.view.setSelectionMode(QAbstractItemView.SingleSelection)  #

        # # widget 창에 꽉 차게 http://bitly.kr/l8mzD7J  https://hoy.kr/dFFaj
        self.view.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        # self.view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # =====
        # size policy : https://hoy.kr/dFFaj
        self.view.setAlternatingRowColors(True)
        self.view.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.view.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum) # Expanding | Minimum | Maximum 

        # header color : https://stackoverflow.com/questions/19198634/pyqt-qtablewidget-horizontalheaderlabel-stylesheet
        stylesheet = """QHeaderView::section{ background-color: #CEECF5; color: blue; }"""
        self.view.horizontalHeader().setStyleSheet(stylesheet)

        # right click menu 추가 : https://freeprog.tistory.com/334 [취미로 하는 프로그래밍 !!!]
        self.view.setContextMenuPolicy(Qt.ActionsContextMenu)
        del_action = QAction("선택행 삭제", self.view)
        self.view.addAction(del_action)
        del_action.triggered.connect(self.del_row)
        # =====
        # # enable sorting : https://codeday.me/ko/qa/20190422/381866.html
        # # 삭제시 df 와 tablevew 간의 row index 일치시키기 위해 죽여놓음
        # self.view.setSortingEnabled(True)
        le = QLineEdit('우클릭: 삭제 / 더블 클릭: 수정')
        le.setReadOnly(True)

        # Qt Style Sheets Examples : https://hoy.kr/d0nYi
        le.setStyleSheet(
                    """QLineEdit { border: 2px solid gray; border-radius: 10px;
                    padding: 2 15px; background: #f0f0f0; color: red; font: bold;
                    selection-background-color: darkgray;} """ )

        self.layout = QVBoxLayout()
        self.layout.addWidget(le)
        
        self.btn1 = QPushButton('저장 후 닫기', self)
        self.btn2 = QPushButton('웹사이트 ID/PW 추가', self)
        self.btn1.setStyleSheet("""QPushButton { background-color: #A9F5F2; color: blue; font: bold;
                                border: 1px solid gray; padding: 5 0px;}""")
        self.btn2.setStyleSheet("""QPushButton { background-color: #A9F5F2; color: blue; font: bold;
                                border: 1px solid gray; padding: 5 0px;}""")
        self.layout.addWidget(self.btn2)  
        
        self.add_table = AddTable(self)
        self.add_table.setHidden(True)              # toggle set
                             
        self.layout.addWidget(self.add_table)
        self.layout.addWidget(self.view)
        self.layout.addWidget(self.btn1) 

        self.setLayout(self.layout)

        # ======== 5. Signal connect Slot (동일 파일 내)
        self.make_connection(self.add_table)
        # self.make_connection_view(self.model)  --- Main __main__ 으로

        # ========
        self.btn1.clicked.connect(self.save_df_to_json)
        self.btn2.clicked.connect(self.add_row)

    @pyqtSlot()
    def del_row(self):
        row_idx = self.view.selectionModel().currentIndex().row() 
        
        self.df = self.df.drop(self.df.index[row_idx], axis=0)
        self.df.reset_index()
        self.model = PandasModel(self.df)
        self.view.setModel(self.model)

        self.btn1.setStyleSheet(
                """QPushButton { background-color: #ffff00; color: blue; font: bold }""") 

        self.emty_site_set = AddTable.item_set - set(self.df['website'].to_list())
 
    @pyqtSlot()  # 엑셀저장  http://bitly.kr/cyM01Yn  
    def save_df_to_json(self):
        #============= 3. Dataframe to original dic_lst_dic : https://hoy.kr/dXq62
        # 1. 값 있는 것
        df_to_dict = self.df.to_dict('split')                    
        _data_lst_lst = df_to_dict['data']
        # 2. 값 없는 것
        empty_site_lst = list(self.emty_site_set)
        empty_site_lst_lst = [[website, "", ""] for website in empty_site_lst]
        # 3. 1+2
        data_lst_lst = _data_lst_lst + empty_site_lst_lst

        web_dic_lst_dic = dict()

        for web, id, pw in data_lst_lst:
            inner_dic = dict()

            inner_dic['id'] = id
            inner_dic['pw'] = pw

            if inner_dic['id'] != "":    
                if web in web_dic_lst_dic.keys():
                    web_dic_lst_dic[web].append(inner_dic)    # nd2 id/pw 이후
                    continue
                web_dic_lst_dic[web] = [inner_dic]            # first id/pw
                continue
            web_dic_lst_dic[web] = []                         # id/pw 가 없는 경우
                
        #============ 4. dict to json
        # fulljs = r'C:\Ataxtech\ATT\Ver1.0\json\web.json'
        self.ddld_dic['idpw'] = web_dic_lst_dic
        with open(fulljs, 'w', encoding='utf-8') as fn:
            json.dump(self.ddld_dic, fn, ensure_ascii=False, indent=4)

        self.btn1.setStyleSheet("""QPushButton { background-color: #A9F5F2; color: blue; font: bold;
                                border: 1px solid gray; padding: 5 0px;}""")
        
        # 2. Signal(json_update_signal) emit
        self.json_update_signal.emit()
    
    @pyqtSlot()
    def add_row(self):
        sender_obj = self.sender()

        if sender_obj.text() == "웹사이트 ID/PW 추가":
            self.add_table.setHidden(False)                 # toggle
            sender_obj.setText("ID/PW 저장")
            # sender_obj.setStyleSheet(
            #         """QPushButton { background-color: #ffff00; color: blue; font: bold }""")
            
        elif sender_obj.text() == "ID/PW 저장":
            # print(self.add_table.website,'===', self.add_table.id, '===', self.add_table.pw)
            self.add_table.setHidden(True)                  # toggle
            sender_obj.setText("웹사이트 ID/PW 추가")
            
            # df에 리스트 바로 붙이기 https://hoy.kr/v8Krj
            if self.add_table.id != "" and self.add_table.pw != "":  # id/pw 모두 입력
                add_df_row_lst = [self.add_table.website, self.add_table.id, self.add_table.pw]
                self.df.loc[len(self.df)+1] = add_df_row_lst
                self.model = PandasModel(self.df)
                self.view.setModel(self.model)
                
                self.add_table.setItem(0, 1, QTableWidgetItem(""))
                self.add_table.setItem(0, 2, QTableWidgetItem(""))

                sender_obj.setStyleSheet(
                    """QPushButton { background-color: #A9F5F2; color: blue; font: bold }""")
         
                self.btn1.setStyleSheet(
                         """QPushButton { background-color: #ffff00; color: blue; font: bold }""")  

                self.emty_site_set = AddTable.item_set - set(self.df['website'].to_list())
                # print(self.emty_site_set)
        
    # 3. Signal connect Slot
    def make_connection(self, signal_emit_object):
        signal_emit_object.pw_changed_signal.connect(self.receive_add_idpw)
    
    # 3. Signal connect Slot
    def make_connection_view(self, signal_emit_object):
        signal_emit_object.view_edit_signal.connect(self.receive_edit_idpw)

    # 3. Signal(json_update_signal) connect Slot
    def make_connection_json_update(self, signal_emit_object):
        signal_emit_object.json_update_signal.connect(self.receive_json_update)
     
    # 4. receive Signal
    @pyqtSlot()
    def receive_add_idpw(self):
        self.btn2.setStyleSheet(
                """QPushButton { background-color: #ffff00; color: blue; font: bold }""")

    # 4. receive Signal
    @pyqtSlot()
    def receive_edit_idpw(self):
        self.btn1.setStyleSheet(
                """QPushButton { background-color: #ffff00; color: blue; font: bold }""") 
               
    # 4. receive Signal(json_update_signal)
    @pyqtSlot()
    def receive_json_update(self):
        self.update_json()
        self.model = PandasModel(self.df)
        self.view.setModel(self.model)

    def update_json(self):
       
        result = ddld_json_to_df()
        self.ddld_dic = result[0]
        self.idpw_dic_lst_dic = result[1]
        self.df = result[2]  

        self.emty_site_set = AddTable.item_set - set(self.df['website'].to_list())

        #============= 3. Dataframe to original dic_lst_dic : https://hoy.kr/dXq62
        # 1. 값 있는 것
        df_to_dict = self.df.to_dict('split')                    
        _data_lst_lst = df_to_dict['data']
        # 2. 값 없는 것
        empty_site_lst = list(self.emty_site_set)
        empty_site_lst_lst = [[website, "", ""] for website in empty_site_lst]
        # 3. 1+2
        data_lst_lst = _data_lst_lst + empty_site_lst_lst

        web_dic_lst_dic = dict()

        for web, id, pw in data_lst_lst:
            inner_dic = dict()

            inner_dic['id'] = id
            inner_dic['pw'] = pw

            if inner_dic['id'] != "":    
                if web in web_dic_lst_dic.keys():
                    web_dic_lst_dic[web].append(inner_dic)    # nd2 id/pw 이후
                    continue
                web_dic_lst_dic[web] = [inner_dic]            # first id/pw
                continue
            web_dic_lst_dic[web] = []                         # id/pw 가 없는 경우
                
        #============ 4. dict to json
        # fulljs = r'C:\Ataxtech\ATT\Ver1.0\json\web.json'
        self.ddld_dic['idpw'] = web_dic_lst_dic
        with open(fulljs, 'w', encoding='utf-8') as fn:
            json.dump(self.ddld_dic, fn, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Ui_WebSetting()
    ex.show()
    sys.exit(app.exec_())
    