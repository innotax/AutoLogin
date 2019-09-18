import os, sys, time, json, zipfile, tkinter

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QDesktopWidget

# 상위폴더 내 파일 import  https://brownbears.tistory.com/296
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))                                   # 1단계 상위폴더
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))) # 2단계 상위폴더

from data import setdata, dictdata
from utils import Util, driverutil
# from utils.driverutil import get_element

get_element = driverutil.get_element

nts_dict, web_dict = setdata.setup_path_json_dict() 


class Nts_Login:
    def __init__(self):
        driver_path = nts_dict['secret']['드라이버경로']    
        driver_name = nts_dict['secret']['크롬드라이버'] 
        driver = driverutil.Get_driver(driver_path, driver_name)
        self.driver = driver.chrome_driver()
        self.driver.get('https://www.hometax.go.kr/')
      
        # 모니터 작은 경우 https://code-examples.net/ko/q/2fbfea
        tk = tkinter.Tk()
        screen_height = tk.winfo_screenheight()
       
        if screen_height <= 900:
            self.driver.maximize_window()

        # input value 입력 변수 셋팅
        self.cta_id = nts_dict['secret']['세무사관리번호']
        self.bs_id = nts_dict['secret']['부서아이디']
        self.super_id = nts_dict['secret']['수퍼아이디'] 
        self.cert_name = nts_dict['secret']['공인인증서명칭']
        self.cta_pw = nts_dict['secret']['세무사비번']
        self.bs_pw = nts_dict['secret']['부서비번'] 
        self.delay_time = float(nts_dict['secret']['딜레이타임'])
        self.cert_pw = nts_dict['secret']['공인인증서비번'] 

        ### element 변수 셋팅
        # click elem
        self.top_login_btn = nts_dict['elem_id']['login']['최상단로그인']
        self.cert_login_btn = nts_dict['elem_id']['login']['인증서로그인']
        self.bs_id_login_btn = nts_dict['elem_id']['login']['부서아이디로그인']
        self.main_zone = nts_dict['메인영역']
        self.cert_zone = nts_dict['elem_id']['login']['공인인증서영역']
        self.cert_name_elem = nts_dict['secret']['공인인증서명칭']           #########
        self.cert_confirm_btn = nts_dict['elem_id']['login']['공인인증서확인']
        self.last_login_btn = nts_dict['elem_id']['login']['최종로그인']
        # input value elem
        self.cta_id_elem = nts_dict['elem_id']['login']['세무사관리번호']
        self.bs_id_elem = nts_dict['elem_id']['login']['부서아이디']
        self.cta_pw_elem = nts_dict['elem_id']['login']['세무사비번']
        self.bs_pw_elem = nts_dict['elem_id']['login']['부서비번']
        self.cert_pw_elem = nts_dict['elem_id']['login']['공인인증서비번']

        time.sleep(self.delay_time + 2)

    # 홈택스 별도페이지
    def path2(self):
        try:
            _ST1BOX = self.driver.find_element_by_id("ST1BOX")  # 종합소득세 신고
            _ST1BOX.click()
            time.sleep(self.delay_time)
            self.loginnts()
        except:
            self.loginnts()
            time.sleep(self.delay_time)

    def loginnts(self):
        
        # 홈텍스로 이동, 상단 로그인
        get_element(self.driver, self.top_login_btn).click()
        # self.driver.implicitly_wait(delay_time)

        # 메인영역
        elem = get_element(self.driver, self.main_zone)
        self.driver.switch_to.frame(elem)
        time.sleep(self.delay_time + 1)
        
        # 관리자인 경우 공인인증서 직접로그인
        if (self.bs_id==self.super_id or self.bs_id==""):
            # get_element(self.driver, self.cert_login_btn).click()
            # 공인인증서 로그인 버튼 : 클릭 안될 때  http://bitly.kr/ckLhMIb  # 자바 명령어 실행
            elem = get_element(self.driver, self.cert_login_btn)           # .click()
            self.driver.execute_script("arguments[0].click();", elem)      # 자바 명령어 실행
            time.sleep(self.delay_time + 3)

        # 부서아이디 유무
        elif self.bs_id !="":
            # 부서아이디 입력
            get_element(self.driver, self.bs_id_elem).send_keys(self.bs_id)

            if self.bs_pw=="":               # 부서비번 없으면
                # 부서 비밀번호 입력 QInputDialog
                app = QApplication(sys.argv)
                inputdlg = Util.InputDlg()
                title = "부서비밀번호 입력!"
                input_label = "부서비밀번호 :"
                bs_pw = inputdlg.initUi(title=title, input_label=input_label)

                self.bs_pw = bs_pw
                nts_dict['secret']['부서비번'] = bs_pw
                # 2. 수정된 딕셔너리를 json 파일로 만들어 저장  
                Util.save_dict_to_json(setdata.full_json_fn, nts_dict)
            else:
                # 부서비밀번호 입력 + 로그인 버튼 클릭
                get_element(self.driver, self.bs_pw_elem).send_keys(self.bs_pw)
                # time.sleep(self.delay_time + 1)
                elem = get_element(self.driver, self.bs_id_login_btn)
                self.driver.execute_script("arguments[0].click();", elem)      # 자바 명령어 실행 http://bitly.kr/ckLhMIb 
                time.sleep(self.delay_time + 3)
        else:
            # 공인인증서 로그인 버튼 : 클릭 안될 때  http://bitly.kr/ckLhMIb  # 자바 명령어 실행
            elem = get_element(self.driver, self.cert_login_btn)           # .click()
            self.driver.execute_script("arguments[0].click();", elem)      # 자바 명령어 실행 http://bitly.kr/ckLhMIb 
            time.sleep(self.delay_time + 3)

        # 공인인증서 영역
        elem = get_element(self.driver, self.cert_zone)
        self.driver.switch_to.frame(elem)
        time.sleep(self.delay_time + 1)
        
        # 공인인증서 선택
        get_element(self.driver, self.cert_name_elem, attribute="title").click()
        # elem = get_element(self.driver, self.cert_name_elem, attribute="title")
        # self.driver.execute_script("arguments[0].click();", elem)      # 자바 명령어 실행 http://bitly.kr/ckLhMIb 
        time.sleep(self.delay_time + 1)

        # 인증서 비밀번호 입력 + 인증서 확인 버튼
        get_element(self.driver, self.cert_pw_elem).send_keys(self.cert_pw)
        get_element(self.driver, self.cert_confirm_btn).click()
        time.sleep(self.delay_time + 1)

        # 팝업창 (세무사관리번호 로그인)
        alert = self.driver.switch_to.alert  # print(alert.text)         
        alert.accept()
        
        # 메인영역
        elem = get_element(self.driver, self.main_zone)
        self.driver.switch_to.frame(elem)
        time.sleep(self.delay_time)

        # 세무대리인 관리번호 비번
        get_element(self.driver, self.cta_id_elem).send_keys(self.cta_id)
        get_element(self.driver, self.cta_pw_elem).send_keys(self.cta_pw)
        # 최종 로그인 버튼
        get_element(self.driver, self.last_login_btn).click()

if __name__ == "__main__":

    login = Nts_Login()
    login.path2()