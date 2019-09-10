import os, sys, time, json
# 폴더 파일 리스트 가져오기 : https://3months.tistory.com/203 
from os import listdir, rename
from os.path import isfile, isdir, join

import pyautogui as m
import pyperclip

import PyQt5
# from PyQt5.Qt import QApplication
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDesktopWidget, QWidget, QDialog, QComboBox, QInputDialog,
                            QPushButton, QRadioButton, QLabel, QLineEdit, QAction, QToolTip, qApp)
from PyQt5.QtWidgets import QMessageBox, QTabWidget, QGridLayout, QGroupBox, QHBoxLayout, QVBoxLayout, QFormLayout
from PyQt5.QtGui import QIcon, QRegExpValidator, QDoubleValidator, QIntValidator, QFont
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QRegExp

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# https://5kyc1ad.tistory.com/326 Copyright (c) 2018 Sanghyeon Jeon
def Mkdirs(filePath):
    # dirPath = os.path.sep.join(filePath.split(os.path.sep)[:-1])
    dirPath = os.path.sep.join(filePath.split(os.path.sep)[:])

    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
## =================

def get_dic_file_path(path):
    """ 경로 받아서 전체경로파일명 딕셔너리 리턴: 파일명(확장자제외): 전체경로 
    """
    from os import listdir, rename
    from os.path import isfile, join
    
    files = [f for f in listdir(path) if isfile(join(path,f))] # 파일 리스트
    dic_file_path = {file.split(".")[0] : join(path, file) for file in files} # 딕셔너리 :  파일명(확장자제외) : 전체경로
    
    return dic_file_path
    
def get_xy(img):
    """ 이미지 파일 식별 및 좌표반환
        import pyautogui as m
    """
    try:
        pos_img = m.locateOnScreen(img)
        x, y = m.center(pos_img)
        return (x,y)
    except Exception as e:
        pass

### 1.1 변수 지정된 경로에 디렉토리가 있는지를 체크하고 없으면 디렉토리를 생성
def make_dirs(base_path, *new_dirs):
    """ 1.1 변수 지정된 경로에 디렉토리가 있는지를 체크하고 없으면 디렉토리를 생성
        첫번째 인수로 전달한 경로(base_path)에 두번째 가변인수(*new_dirs)로 전달한 디렉토리 생성 
        dir은 영문 권장, 가변인수는 str, tuple, list 가능
        ex) base_path = "C:\\zz"   # 내문서 : os.path.expanduser("~\\documents") / 바탕화면 Desktop / 다운로드 Downloads
            # base_path = os.path.expanduser("~\\documents") # 내문서
            new_dirs = ['1','2','3'] 
            make_sub_dirs(base_path, *new_dirs)
            >> ['C:\\zz\\1', 'C:\\zz\\2', 'C:\\zz\\3'] 
    """
    import os
    base_path = base_path
    lst_new_dir = []
    
    for d in new_dirs:
        new_dir = os.path.join(base_path, d)
        
        if os.path.isdir(new_dir):
            lst_new_dir.append(new_dir)
            continue
        elif not os.path.isdir(new_dir):
            os.mkdir(new_dir)
            lst_new_dir.append(new_dir)
            
    return lst_new_dir

def make_sub_dirs(base_path, *new_dirs):
    """ 1.2 변수 지정된 경로에 디렉토리가 있는지를 체크하고 없으면 순차적 하위 디렉토리를 생성
        첫번째 인수로 전달한 경로(base_path)에 두번째 가변인수(*new_dirs)로 전달한 디렉토리를 순차적으로 생성 
        dir은 영문 권장, 가변인수는 str, tuple, list 가능
        ex) base_path = "C:\\zz"   # 내문서 : os.path.expanduser("~\\documents") / 바탕화면 Desktop / 다운로드 Downloads 
            # base_path = os.path.expanduser("~\\documents") # 내문서
            new_dirs = ['1','2','3'] 
            make_sub_dirs(base_path, *new_dirs)
            >> ['C:\\zz\\1', 'C:\\zz\\1\\2', 'C:\\zz\\1\\2\\3']        
    """
    import os
    base_path = base_path 
    lst_new_dir = []
    
    for d in new_dirs:
        new_dir = os.path.join(base_path, d)
        
        if os.path.isdir(new_dir):
            base_path += "\\"+d
            lst_new_dir.append(new_dir)
            continue
        elif not os.path.isdir(new_dir):
            os.mkdir(new_dir)
            base_path += "\\"+d
            lst_new_dir.append(new_dir)
            
    return lst_new_dir
##############################           
### json 파일 다루기 
class JsonConverter(object):
    """ func(param) : use
            json_to_dict(jsonfile): json 파일을 받아 딕셔너리 객체를 반환한다.
            dict_to_json(jsonfile, dic_obj): 딕셔너리 객체를 json 파일로 저장한다. 
            lstOFdic_to_tupKeysVals(list_of_dict): 리스트[{딕셔너리...},...] 를 key값을 제외한 value값 이중리스트[[v1,v2,..],...]로 변환후 tuple(keys, list_of_list)반환
            lstOFlst_to_lstOFdic(key_list, list_of_list): 이차원(이중) 리스트의 내부 리스트를 전달된 key_list로 딕셔너리로 변환후 리스트[딕셔너리] 반환
    """   
    def __init__(self):
        pass
        
    def json_to_dict(self, jsonfile):
        """ json 파일을 받아 딕셔너리 객체를 반환한다.
            param : jsonfile = full_path_jsonfile_name
        """
        with open(fulljs, encoding='utf-8') as fn:
            dic_obj = json.load(fn)
        return dic_obj

    def dict_to_json(self, dic_obj, jsonfile):
        """ 딕셔너리 객체를 json 파일로 저장한다.
            param : jsonfile = full_path_jsonfile_name
                    dic_obj = python 딕셔너리 type
        """
        with open(jsonfile, 'w', encoding='utf-8') as fn:
            json.dump(dic_obj, fn, ensure_ascii=False, indent=4)

    def lstOFdic_to_tupKeysVals(self, list_of_dict=None): 
        """ 파이썬 코딩의 기술 79p 동적 기본 인수를 지정하려면 None과 docstring를 사용하자
            리스트[{딕셔너리...},...] 를 key값을 제외한 value값 이중리스트[[v1,v2,..],...]로 변환후 tuple(keys, list_of_list)반환
            Caution : len(key_list) == len(list_of_list[i]) 
            parm : list_of_dict = [{'id': 'user1_id', 'pw': 'user1_pw'},
                                   {'id': 'user1_id', 'pw': 'user1_pw'}]                 
            return(tuple) : key_list = ['id', 'pw']
                            list_of_list = [['user1_id','user1_pw'],
                                            ['user2_id','user2_pw']]       
        """
        if list_of_dict:
            key_list = list(list_of_dict[0].keys())
            list_of_list = [[dic[key] for key in list_of_dict[0].keys()] for dic in list_of_dict]
            return (key_list, list_of_list)
        return ([], [['ID입력요망', 'PW입력요망']])

    def lstOFlst_to_lstOFdic(self, key_list, list_of_list):
        """ 이차원(이중) 리스트의 내부 리스트를 전달된 key_list로 딕셔너리로 변환후 리스트[딕셔너리] 반환
            Caution : len(key_list) == len(list_of_list[i])
            parm : key_list = ['id', 'pw']
                   list_of_list = [['user1_id','user1_pw'],
                                   ['user2_id','user2_pw']]
            return : [{'id': 'user1_id', 'pw': 'user1_pw'},
                      {'id': 'user1_id', 'pw': 'user1_pw'}]
        """
        list_of_dict = [dict(zip(key_list, lst)) for lst in list_of_list]
        return list_of_dict

def save_dict_to_json(full_json_fn, dict_obj):
    """딕셔너리 객체를 json 파일로 저장한다. 
    :param  full_json_fn: 저장경로+ {}.json "C:/zz/data.json"
            dict_obj: dict 파이썬 객체 
    :return full_json_fn 
    """
    with open(full_json_fn, 'w', encoding='utf-8') as fn:
        json.dump(dict_obj, fn, ensure_ascii=False, indent=4)
    
    return full_json_fn

def json_to_dict(full_json_fn):
    """json 파일을 받아 딕셔너리 객체를 반환한다. 
    :param  full_json_fn: json 파일명(경로포함) "C:/zz/data.json"        
    :return dict_data: dict 파이썬 객체 
    """
    with open(full_json_fn, encoding='utf-8') as fn:
        dict_obj = json.load(fn)
    
    return dict_obj

# QT 에러메세지 
class Errpop(QWidget):
    def __init__(self):
        super().__init__()   
        rect = QDesktopWidget().availableGeometry()   # 작업표시줄 제외한 화면크기 반환
        max_x = rect.width()
        max_y = rect.height()

        width, height = 350 , 250
        left = max_x - width 
        top = max_y - height
        self.setGeometry(left, top, width, height)     

    def critical_pop(self, msg):    
        msg = msg
        QMessageBox.critical(self, '에러 메세지', msg, QMessageBox.Ok)

# QMessageBox : return True / False
class MsgBoxTF(QMessageBox):
    '''param : title="QMessageBox", msg=None
       return : True / False
    '''
    def __init__(self, title="QMessageBox", msg=None):
        super().__init__()
        self.title = title
        self.msg = msg

        rect = QDesktopWidget().availableGeometry()   # 작업표시줄 제외한 화면크기 반환
        max_x = rect.width()
        max_y = rect.height()

        self.width = 320
        self.height = 200
        # self.left = max_x - self.width 
        # self.top = max_y - self.height
        # 윈도우 중간
        self.left = max_x / 2
        self.top = max_y /2 
        
        # self.initUI()
        
    def initUI(self):
        # self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        buttonReply = QMessageBox.question(self, self.title, self.msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if buttonReply == QMessageBox.Yes:
            return True
            # print('Yes clicked.')
        else:
            return False
            # print('No clicked.')

class InputDlg(QInputDialog):
    def __init__(self, parent=None):
        super().__init__()

        rect = QDesktopWidget().availableGeometry()   # 작업표시줄 제외한 화면크기 반환
        max_x = rect.width()
        max_y = rect.height()

        width, height = 350 , 250
        left = max_x - width 
        top = max_y - height
        self.setGeometry(left, top, width, height)  
        # self.show()
            
    def initUi(self, title="", input_label="입력값 :"):
        text, ok = QInputDialog.getText(self, title, input_label)
        if ok:
            return text #, sys.exit(self) 
        else:
            pass
            # sys.exit(self)


