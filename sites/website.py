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
# ==================


class NaverMail(object):
    """ https://github.com/lumyjuwon/NaverCaptcha
        https://5kyc1ad.tistory.com/326 Copyright (c) 2018 Sanghyeon Jeon
    """
    def __init__(self, user_id, user_pw):
        self.ID = user_id
        self.PW = user_pw

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


if __name__ == "__main__":
    id = 'innotax14'
    pw = 'YDI102030**'
    # id = 'taxkmj'
    # pw = 'ekthfqksvh'
    naver = NaverMail(id, pw)
    naver.clipboard_login(naver.ID, naver.PW)

