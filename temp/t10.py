from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import pandas as pd
import sys, os, json

# 상위폴더 내 파일 import  https://brownbears.tistory.com/296
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from utils.pandasmodel import PandasModel, DataFrameModel


#============== 1. json to dic
fulljs = r'C:\Ataxtech\ATT\Ver1.0\json\web.json'

with open(fulljs, encoding='utf-8') as fn:
    dic = json.load(fn)                      # dic : dic_dic_lst_dic
idpw_dic_lst_dic = dic['idpw']               # idpw_dic_lst_dic : dic_lst_dic

# print("  1. >> type(idpw_dic_lst_dic) : ", type(idpw_dic_lst_dic), "="*100)

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



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # model = PandasModel(df)
    model = PandasModel(web_id_pw)
    # view = QtWidgets.QTableWidget()
    view = QtWidgets.QTableView()
    view.setModel(model)
    view.resize(800, 600)
    view.show()
    sys.exit(app.exec_())