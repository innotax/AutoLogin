import os, sys, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# 상위폴더 내 파일 import  https://brownbears.tistory.com/296
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))                                   # 1단계 상위폴더
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))) # 2단계 상위폴더

from data import setdata, dictdata
from utils import Util, driverutil
from utils.driverutil import DriverUtils
from utils.winkeyboard import WinKeyboard

# 네이버 캡차(Captcha) 무력화 https://hyrama.com/?p=693
### 자동입력방지문자 우회 https://sab-jil.tistory.com/2

# ===== Config =====
nts_dict, web_dict = setdata.setup_path_json_dict() 
FULLPATH_CHROME_DRIVER = os.path.join(nts_dict['secret']['드라이버경로'], "chromedriver.exe" )
DELAY = 0.5
# ==================


class MyChromeDriver(object):
    def __init__(self):
        # Web Driver 옵션 추가
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        # options.add_argument("--app=https://google.com") # win32api_login 사용 시 반드시 활성화
        options.add_argument("disable-gpu")
        options.add_argument('window-size=1920x1080')
        options.add_argument("lang=ko_KR")
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36')
        # options.add_argument("user-data-dir=\\user-data\\naver\\")
        self.driver = webdriver.Chrome(FULLPATH_CHROME_DRIVER, chrome_options=options)

class NaverMail(MyChromeDriver):
    """ https://github.com/lumyjuwon/NaverCaptcha
        https://5kyc1ad.tistory.com/326 Copyright (c) 2018 Sanghyeon Jeon
    """
    def __init__(self, user_id, user_pw):
        super().__init__()
        self.ID = user_id
        self.PW = user_pw

        self.driver.get('https://naver.com')

        self.explicit_wait_time = 0.5
        self.driver_utils = DriverUtils(self.driver)
        self.keyboard = WinKeyboard()

    def clipboard_login(self, user_id, user_pw):
        self.driver.find_element_by_xpath('//*[@id="account"]/div/a/i').click()
        time.sleep(self.explicit_wait_time)

        self.driver_utils.clipboard_input('//*[@id="id"]', user_id)
        self.driver_utils.clipboard_input('//*[@id="pw"]', user_pw)

        self.driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
        time.sleep(self.explicit_wait_time)
        # 새로운 기기등록 창 뜨면 등록안함 클릭 is_displayed
        try:   
            elem = self.driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/span[2]/a')
            if elem.is_displayed():
                elem.click()
        except Exception as e:  # NoSuchElementException
            print(e)
            pass
        time.sleep(self.explicit_wait_time)
        self.driver.get('https://mail.naver.com')

    def win32api_login(self, user_id, user_pw):
        self.driver.find_element_by_xpath('//*[@id="account"]/div/a/i').click()
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="id"]').click()
        self.keyboard.press(list(user_id))
        self.driver.find_element_by_xpath('//*[@id="pw"]').click()
        self.keyboard.press(list(user_pw))
        self.driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()

    def send_keys_login(self, user_id, user_pw):
        self.driver.find_element_by_xpath('//*[@id="account"]/div/a/i').click()
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="id"]').send_keys(user_id)
        self.driver.find_element_by_xpath('//*[@id="pw"]').send_keys(user_pw)
        self.driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()

class Hanbiro(MyChromeDriver):
    def __init__(self, user_id, user_pw):
        super().__init__()
        self.ID = user_id
        self.PW = user_pw

        self.driver.get('http://innotax.hanbiro.net/ngw/app/#/sign')
        self.driver_utils = DriverUtils(self.driver)
        time.sleep(DELAY)
    
    def login(self, user_id, user_pw):
        self.driver.find_element_by_xpath('//*[@id="log-userid"]').clear()
        self.driver.find_element_by_xpath('//*[@id="log-userid"]').send_keys(user_id)
        time.sleep(DELAY)

        elem = self.driver.find_element_by_xpath('//*[@id="iframeLoginPassword"]')
        self.driver.switch_to.frame(elem)
        time.sleep(DELAY)

        self.driver.find_element_by_xpath('//*[@id="p"]').send_keys(user_pw)
        self.driver.switch_to_default_content()

        self.driver.find_element_by_xpath('//*[@id="btn-log"]').click()

class Nate(MyChromeDriver):
    def __init__(self, user_id, user_pw):
        super().__init__()
        self.ID = user_id
        self.PW = user_pw

        self.driver.get('https://www.nate.com/')
        self.driver_utils = DriverUtils(self.driver)
        time.sleep(DELAY)
    
    def login(self, user_id, user_pw):
        self.driver.find_element_by_xpath('//*[@id="ID"]').clear()
        self.driver.find_element_by_xpath('//*[@id="ID"]').send_keys(user_id)
        time.sleep(DELAY)

        self.driver.find_element_by_xpath('//*[@id="PASSDM"]').send_keys(user_pw)
        time.sleep(DELAY)
        self.driver.find_element_by_xpath('//*[@id="btnLOGIN"]').click()
        self.driver.get('https://mail3.nate.com/')

class Daum(MyChromeDriver):
    def __init__(self, user_id, user_pw):
        super().__init__()
        self.ID = user_id
        self.PW = user_pw

        self.driver.get('https://logins.daum.net/accounts/signinform.do?url=https%3A%2F%2Fwww.daum.net%2F')
        self.driver_utils = DriverUtils(self.driver)
        time.sleep(DELAY)
    
    def login(self, user_id, user_pw):
        self.driver.find_element_by_xpath('//*[@id="id"]').clear()
        self.driver.find_element_by_xpath('//*[@id="id"]').send_keys(user_id)
        time.sleep(DELAY)

        self.driver.find_element_by_xpath('//*[@id="inputPwd"]').send_keys(user_pw)
        time.sleep(DELAY)
        self.driver.find_element_by_xpath('//*[@id="loginBtn"]').click()
        self.driver.get('https://mail.daum.net/')

class Bizforms(MyChromeDriver):
    def __init__(self, user_id, user_pw):
        super().__init__()
        self.ID = user_id
        self.PW = user_pw

        self.driver.get('http://www.bizforms.co.kr/')
        self.driver_utils = DriverUtils(self.driver)
        time.sleep(DELAY)
    
    def login(self, user_id, user_pw):
        self.driver.find_element_by_xpath('//*[@id="main2015_center"]/section[1]/dl[1]/dd[1]/div[2]/form/table/tbody/tr/td[1]/div[1]/input').clear()
        self.driver.find_element_by_xpath('//*[@id="main2015_center"]/section[1]/dl[1]/dd[1]/div[2]/form/table/tbody/tr/td[1]/div[1]/input').send_keys(user_id)
        time.sleep(DELAY)

        self.driver.find_element_by_xpath('//*[@id="main2015_center"]/section[1]/dl[1]/dd[1]/div[2]/form/table/tbody/tr/td[1]/div[2]/input').send_keys(user_pw)
        time.sleep(DELAY)
        self.driver.find_element_by_xpath('//*[@id="main2015_center"]/section[1]/dl[1]/dd[1]/div[2]/form/table/tbody/tr/td[2]/a').click()

class Etaxkorea(MyChromeDriver):
    def __init__(self, user_id, user_pw):
        super().__init__()
        self.ID = user_id
        self.PW = user_pw

        self.driver.get('http://www.etaxkorea.net/')
        self.driver_utils = DriverUtils(self.driver)
        time.sleep(DELAY)
    
    def login(self, user_id, user_pw): 
        self.driver.find_element_by_xpath('//*[@id="body"]/div[3]/div[1]/div/form/input[3]').clear()
        self.driver.find_element_by_xpath('//*[@id="body"]/div[3]/div[1]/div/form/input[3]').send_keys(user_id)
        time.sleep(DELAY)

        self.driver.find_element_by_xpath('//*[@id="body"]/div[3]/div[1]/div/form/input[4]').send_keys(user_pw)
        time.sleep(DELAY)
        self.driver.find_element_by_xpath('//*[@id="body"]/div[3]/div[1]/div/form/a/img').click()

class TheBill(MyChromeDriver):
    def __init__(self, user_id, user_pw):
        super().__init__()
        self.ID = user_id
        self.PW = user_pw

        self.driver.get('https://www.thebill.co.kr:444/main.jsp')
        self.driver_utils = DriverUtils(self.driver)
        time.sleep(DELAY)
    
    def login(self, user_id, user_pw):
        self.driver.find_element_by_xpath('//*[@id="loginid"]').clear()
        self.driver.find_element_by_xpath('//*[@id="loginid"]').send_keys(user_id)
        time.sleep(DELAY)

        self.driver.find_element_by_xpath('//*[@id="loginpw"]').clear()
        self.driver.find_element_by_xpath('//*[@id="loginpw"]').send_keys(user_pw)
        time.sleep(DELAY)
        self.driver.find_element_by_xpath('//*[@id="btnLogin"]').click()
        # self.driver.get('https://mail3.nate.com/')

if __name__ == "__main__":
    # id = 'innotax14'
    # pw = 'YDI102030**'
    # id = 'taxkmj'
    # pw = 'ekthfqksvh'
    # naver = NaverMail(id, pw)
    # naver.clipboard_login(naver.ID, naver.PW)

    # id = 'sgh0'
    # pw = 'innotax1260!'
    # hanbiro = Hanbiro(id, pw)
    # hanbiro.login(hanbiro.ID, hanbiro.PW)

    # id = 'innotax14'
    # pw = 'YDI102030**'
    # nate = Nate(id, pw)
    # nate.login(nate.ID, nate.PW)

    # id = 'taxkmj'
    # pw = 'ekthfqksvh'
    # daum = Daum(id, pw)
    # daum.login(daum.ID, daum.PW)

    # id = 'innotax14'
    # pw = 'qwer1234'
    # bizforms = Bizforms(id, pw)
    # bizforms.login(bizforms.ID, bizforms.PW)

    # id = 'ctajung47'
    # pw = 'daeho1260'
    # etaxkorea = Etaxkorea(id, pw)
    # etaxkorea.login(etaxkorea.ID, etaxkorea.PW)

    id = 'ctajung47'
    pw = 'daeho1260'
    theBill = TheBill(id, pw)
    theBill.login(theBill.ID, theBill.PW)

