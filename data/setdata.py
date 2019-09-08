import os, sys, time, json, zipfile

# 상위폴더 내 파일 import  https://brownbears.tistory.com/296
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))) # 2단계 상위폴더

import data.dictdata
# from data import dictdata
from utils import Util


# ===== Config =====
INFOTECH_DLL_PATH = r'C:\InfoTech\common'
DRIVER_PATH = r'C:\Ataxtech\ATT\Ver1.0\driver'
JSON_PATH = r'C:\Ataxtech\ATT\Ver1.0\json'
NTS_JSON_FILE = 'nts.json'
WEB_JSON_FILE = 'web.json'
FULLPATH_NTS_JSON = os.path.join(JSON_PATH, NTS_JSON_FILE)
FULLPATH_WEB_JSON = os.path.join(JSON_PATH, WEB_JSON_FILE)
# ==================

def setup_path_json_dict():
    FULLPATH_NTS_JSON = os.path.join(JSON_PATH, NTS_JSON_FILE)
    FULLPATH_WEB_JSON = os.path.join(JSON_PATH, WEB_JSON_FILE)

    # JSON_PATH에 json 파일이 있으면 dic 변환후 리턴
    if os.path.exists(FULLPATH_NTS_JSON) and os.path.exists(FULLPATH_WEB_JSON) :
        # 3. 저장된 json 파일을 파이썬 객체(딕셔너리)로...
        with open(FULLPATH_NTS_JSON, encoding='utf-8') as fn:
            nts_dict = json.load(fn) 
        
        with open(FULLPATH_WEB_JSON, encoding='utf-8') as fn:
            web_dict = json.load(fn)
        
        return nts_dict, web_dict

    else:
        # DRIVER_PATH에 크롬드라이버, 인포텍모듈설치파일, icon파일 압축 풀기 : 압축파일은 실행파일(atmui.py) 동일경로에...
        if not os.path.exists(DRIVER_PATH):
            Util.Mkdirs(DRIVER_PATH)
            print(">"*5, os.getcwd())
            with zipfile.ZipFile(os.path.join(os.getcwd(), "driver_iftsetup.zip")) as zf:
                zf.extractall(DRIVER_PATH)

        # 1.JSON_PATH 만들고 2.dict 리턴 받아 업데이트 후 3.json 파일 생성 
        if not os.path.exists(JSON_PATH):
            Util.Mkdirs(JSON_PATH)
            nts_dict = data.dictdata.get_nts_dict()
            web_dict = data.dictdata.get_web_dict()
            nts_dict['secret']['드라이버경로'] = DRIVER_PATH
            web_dict['드라이버경로'] = DRIVER_PATH

            with open(os.path.join(JSON_PATH, NTS_JSON_FILE), 'w', encoding='utf-8') as fn:
                json.dump(nts_dict, fn, ensure_ascii=False, indent=4)

            with open(os.path.join(JSON_PATH, WEB_JSON_FILE), 'w', encoding='utf-8') as fn:
                json.dump(web_dict, fn, ensure_ascii=False, indent=4)

        elif os.path.exists(JSON_PATH):
            if not os.path.exists(FULLPATH_NTS_JSON):
                nts_dict = data.dictdata.get_nts_dict()
                nts_dict['secret']['드라이버경로'] = DRIVER_PATH

                with open(os.path.join(JSON_PATH, NTS_JSON_FILE), 'w', encoding='utf-8') as fn:
                    json.dump(nts_dict, fn, ensure_ascii=False, indent=4)

            if not os.path.exists(FULLPATH_WEB_JSON):
                web_dict = data.dictdata.get_web_dict()
                web_dict['드라이버경로'] = DRIVER_PATH

                with open(os.path.join(JSON_PATH, WEB_JSON_FILE), 'w', encoding='utf-8') as fn:
                    json.dump(web_dict, fn, ensure_ascii=False, indent=4)

    return nts_dict, web_dict






        
        
        

        



# def setup_path_json_dict():   
#     """ 앱 경로설정
#     """
#     """ 인포텍 모쥴 설치
#     if not os.path.isdir(ift_path):
#         import subprocess
#         ''' atmui.py 와 동일한 경로에 iftNxService_setup_20190304.exe 저장
#         '''
#         full_ift_setup_path = os.path.join(os.getcwd(), 'iftNxService_setup_20190304.exe') 
#         PIPE = subprocess.PIPE
#         subprocess.Popen(full_ift_setup_path, stdin=PIPE, stdout=PIPE)
#     """
#     # json 파일이 있으면 dic 변환후 리턴
#     if os.path.isfile(full_json_fn) and os.path.isfile(full_web_json_fn) :
#         # 3. 저장된 json 파일을 파이썬 객체(딕셔너리)로...
#         with open(full_json_fn, encoding='utf-8') as fn:
#             nts_dict = json.load(fn) 
#         # 3. 저장된 web json 파일을 파이썬 객체(딕셔너리)로...
#         with open(full_web_json_fn, encoding='utf-8') as fn:
#             web_dict = json.load(fn)
        
#         return nts_dict, web_dict
        
#     else:
#         try:
#             if not os.path.isdir(att_path):
#                 Util.make_sub_dirs(root_path, att_dir)
#         except:
#             pass

#         try:
#             if not os.path.isdir(main_path):
#                 Util.make_sub_dirs(att_path, main_dir)
#         except:
#             pass

#         # 앱 경로에 하위 경로 설정하고 json 파일 생성후 생성된 json 파일에서 변수로 활용할 파이썬 객체 (nts_dict) 생성
#         try:
#             if not os.path.isdir(st1_app_path):
#                 # 1. 하위 APP 디렉토리 없으면 만들고
#                 Util.make_sub_dirs(main_path, *st1_app_dir)
#                 Util.make_sub_dirs(st1_app_path, "driver") 

#                 # 1.1 크롬드라이버, 인포텍 모쥴 설치(exe 파일과 zip 파일을 같은 경로에...)
#                 try:
#                     with zipfile.ZipFile(os.path.join(os.getcwd(), "driver_iftsetup.zip")) as zf:
#                         zf.extractall(driver_path)
#                 except:
#                     pass
                
#                 # 2. 딕셔너리를 json 파일로 만들어 저장
#                 nts_dict = data.dictdata.get_nts_dict()
                
#                 nts_dict['secret']['드라이버경로'] = driver_path      
#                 with open(full_json_fn, 'w', encoding='utf-8') as fn:
#                     json.dump(nts_dict, fn, ensure_ascii=False, indent=4)
#                     # json_data = json.dumps(_dict_data, ensure_ascii=False, indent=4)

#                 # 3. 저장된 json 파일을 파이썬 객체(딕셔너리)로...
#                 with open(full_json_fn, encoding='utf-8') as fn:
#                     nts_dict = json.load(fn)

#                 # 2. web 딕셔너리를 json 파일로 만들어 저장
#                 web_dict = data.dictdata.get_web_dict()    
#                 with open(full_web_json_fn, 'w', encoding='utf-8') as fn:
#                     json.dump(web_dict, fn, ensure_ascii=False, indent=4)
#                     # json_data = json.dumps(_dict_data, ensure_ascii=False, indent=4)

#                 # 3. 저장된 web json 파일을 파이썬 객체(딕셔너리)로...
#                 with open(full_web_json_fn, encoding='utf-8') as fn:
#                     web_dict = json.load(fn)

#             elif os.path.isdir(st1_app_path):
                
#                 if not os.path.isfile(full_json_fn):
#                 # 2. 딕셔너리를 json 파일로 만들어 저장
#                     nts_dict = data.dictdata.get_nts_dict()  
#                     nts_dict['secret']['드라이버경로'] = driver_path         
#                     with open(full_json_fn, 'w', encoding='utf-8') as fn:
#                         json.dump(nts_dict, fn, ensure_ascii=False, indent=4)
#                         # json_data = json.dumps(_dict_data, ensure_ascii=False, indent=4)

#                     # 3. 저장된 json 파일을 파이썬 객체(딕셔너리)로...
#                     with open(full_json_fn, encoding='utf-8') as fn:
#                         nts_dict = json.load(fn) 

#                 elif os.path.isfile(full_json_fn):
#                     # 3. 저장된 json 파일을 파이썬 객체(딕셔너리)로...
#                     with open(full_json_fn, encoding='utf-8') as fn:
#                         nts_dict = json.load(fn) 
#                 # web
#                 if not os.path.isfile(full_web_json_fn):
#                     # 2. web 딕셔너리를 json 파일로 만들어 저장
#                     web_dict = data.dictdata.get_web_dict()    
#                     with open(full_web_json_fn, 'w', encoding='utf-8') as fn:
#                         json.dump(web_dict, fn, ensure_ascii=False, indent=4)
#                         # json_data = json.dumps(_dict_data, ensure_ascii=False, indent=4)

#                     # 3. 저장된 web json 파일을 파이썬 객체(딕셔너리)로...
#                     with open(full_web_json_fn, encoding='utf-8') as fn:
#                         web_dict = json.load(fn) 

#                 elif os.path.isfile(full_json_fn):
#                     # 3. 저장된 web json 파일을 파이썬 객체(딕셔너리)로...
#                     with open(full_web_json_fn, encoding='utf-8') as fn:
#                         web_dict = json.load(fn) 
#         except:
#             pass
#         finally:
#             return (nts_dict , web_dict)


if __name__ == '__main__':
    print('start')
    nts_dic, web_dict = setup_path_json_dict()
    print(web_dict)