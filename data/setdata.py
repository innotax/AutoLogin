import os, sys, time, json, zipfile

# 상위폴더 내 파일 import  https://brownbears.tistory.com/296
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))) # 2단계 상위폴더

import data
# from data import data
from utils import Util

# 처음시작시 경로설정
root_path = "C:\\"
ift_dir = "Infotech"                  # 스크래핑 모듈
ift_path = os.path.join(root_path, ift_dir)
att_dir = "Ataxtech"
att_path = os.path.join(root_path, att_dir)
main_dir = "AutoLogin"
main_path = os.path.join(att_path, main_dir)          # APP 저장경로
st1_app_dir = ['loginAPP', 'data']
st1_app_path = os.path.join(main_path, st1_app_dir[0]) # 첫번째앱 저장경로
driver_path = os.path.join(st1_app_path, "driver")    # 크롬드라이버 저장경로
data_path = os.path.join(st1_app_path, "data")        # json 파일 등 저장경로
json_fn = "data.json"                                 # 
full_json_fn = os.path.join(data_path, json_fn)       # json 파일 full 경로

web_json_fn = "web.json"  
full_web_json_fn = os.path.join(data_path, web_json_fn) 

def set_path_make_json_return_dic():   
    """ 앱 경로설정
    """
    """ 인포텍 모쥴 설치
    if not os.path.isdir(ift_path):
        import subprocess
        ''' atmui.py 와 동일한 경로에 iftNxService_setup_20190304.exe 저장
        '''
        full_ift_setup_path = os.path.join(os.getcwd(), 'iftNxService_setup_20190304.exe') 
        PIPE = subprocess.PIPE
        subprocess.Popen(full_ift_setup_path, stdin=PIPE, stdout=PIPE)
    """
    # json 파일이 있으면 dic 변환후 리턴
    if os.path.isfile(full_json_fn) and os.path.isfile(full_web_json_fn) :
        # 3. 저장된 json 파일을 파이썬 객체(딕셔너리)로...
        with open(full_json_fn, encoding='utf-8') as fn:
            nts_dict = json.load(fn) 
        # 3. 저장된 web json 파일을 파이썬 객체(딕셔너리)로...
        with open(full_web_json_fn, encoding='utf-8') as fn:
            web_dict = json.load(fn)

        return nts_dict, web_dict
        
    else:
        try:
            if not os.path.isdir(att_path):
                Util.make_sub_dirs(root_path, att_dir)
        except:
            pass

        try:
            if not os.path.isdir(main_path):
                Util.make_sub_dirs(att_path, main_dir)
        except:
            pass

        # 앱 경로에 하위 경로 설정하고 json 파일 생성후 생성된 json 파일에서 변수로 활용할 파이썬 객체 (nts_dict) 생성
        try:
            if not os.path.isdir(st1_app_path):
                # 1. 하위 APP 디렉토리 없으면 만들고
                Util.make_sub_dirs(main_path, *st1_app_dir)
                Util.make_sub_dirs(st1_app_path, "driver") 

                # 1.1 크롬드라이버, 인포텍 모쥴 설치(exe 파일과 zip 파일을 같은 경로에...)
                try:
                    with zipfile.ZipFile(os.path.join(os.getcwd(), "driver_iftsetup.zip")) as zf:
                        zf.extractall(driver_path)
                except:
                    pass

                # 2. 딕셔너리를 json 파일로 만들어 저장
                nts_dict = data.get_nts_dict()
                nts_dict['secret']['드라이버경로'] = driver_path      
                with open(full_json_fn, 'w', encoding='utf-8') as fn:
                    json.dump(nts_dict, fn, ensure_ascii=False, indent=4)
                    # json_data = json.dumps(_dict_data, ensure_ascii=False, indent=4)

                # 3. 저장된 json 파일을 파이썬 객체(딕셔너리)로...
                with open(full_json_fn, encoding='utf-8') as fn:
                    nts_dict = json.load(fn)

                # 2. web 딕셔너리를 json 파일로 만들어 저장
                web_dict = data.get_web_dict()
                nts_dict['secret']['드라이버경로'] = driver_path      
                with open(full_web_json_fn, 'w', encoding='utf-8') as fn:
                    json.dump(web_dict, fn, ensure_ascii=False, indent=4)
                    # json_data = json.dumps(_dict_data, ensure_ascii=False, indent=4)

                # 3. 저장된 web json 파일을 파이썬 객체(딕셔너리)로...
                with open(full_web_json_fn, encoding='utf-8') as fn:
                    web_dict = json.load(fn)

            elif os.path.isdir(st1_app_path):
                if not os.path.isfile(full_json_fn):
                # 2. 딕셔너리를 json 파일로 만들어 저장
                    nts_dict = data.get_nts_dict()        
                    with open(full_json_fn, 'w', encoding='utf-8') as fn:
                        json.dump(nts_dict, fn, ensure_ascii=False, indent=4)
                        # json_data = json.dumps(_dict_data, ensure_ascii=False, indent=4)

                    # 3. 저장된 json 파일을 파이썬 객체(딕셔너리)로...
                    with open(full_json_fn, encoding='utf-8') as fn:
                        nts_dict = json.load(fn) 

                elif os.path.isfile(full_json_fn):
                    # 3. 저장된 json 파일을 파이썬 객체(딕셔너리)로...
                    with open(full_json_fn, encoding='utf-8') as fn:
                        nts_dict = json.load(fn) 
                # web
                if not os.path.isfile(full_web_json_fn):
                    # 2. web 딕셔너리를 json 파일로 만들어 저장
                    web_dict = data.get_web_dict()
                    nts_dict['secret']['드라이버경로'] = driver_path      
                    with open(full_web_json_fn, 'w', encoding='utf-8') as fn:
                        json.dump(web_dict, fn, ensure_ascii=False, indent=4)
                        # json_data = json.dumps(_dict_data, ensure_ascii=False, indent=4)

                    # 3. 저장된 web json 파일을 파이썬 객체(딕셔너리)로...
                    with open(full_web_json_fn, encoding='utf-8') as fn:
                        web_dict = json.load(fn) 

                elif os.path.isfile(full_json_fn):
                    # 3. 저장된 web json 파일을 파이썬 객체(딕셔너리)로...
                    with open(full_web_json_fn, encoding='utf-8') as fn:
                        web_dict = json.load(fn) 
        except:
            pass
        finally:
            return (nts_dict , web_dict)


if __name__ == '__main__':
    
    nts_dic, web_dict = set_path_make_json_return_dic()
    print(web_dict)