import os, sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# 상위폴더 내 파일 import  https://brownbears.tistory.com/296
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))                                   # 1단계 상위폴더
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))) # 2단계 상위폴더

from data import setdata, data
from utils import Util, driverutil

# 네이버 캡차(Captcha) 무력화 https://hyrama.com/?p=693
### 자동입력방지문자 우회 https://sab-jil.tistory.com/2

# chrome_path = r'C:\zz\NTS\driver\chromedriver.exe'
# driver = webdriver.Chrome(chrome_path)
# driver.implicitly_wait(3)
# driver.get('https://nid.naver.com/nidlogin.login')

nts_dict, web_dict = setdata.set_path_make_json_return_dic() 

class NaverLogin:
    def __init__(self, id="innotax14", pw=""):
        driver_path = nts_dict['secret']['드라이버경로']    
        driver_name = nts_dict['secret']['크롬드라이버'] 
        driver = driverutil.Get_driver(driver_path, driver_name)
        driver = driver.chrome_driver()
        driver.get('https://nid.naver.com/nidlogin.login')
        self.id = id
        self.pw = pw

        # driver.find_element_by_id('id').send_keys('taxkmj')
        # driver.find_element_by_id('pw').send_keys('ekthfqksvh')

        # id = 'taxkmj'
        # pw = 'ekthfqksvh'
        driver.execute_script("document.getElementsByName('id')[0].value=\'" + id + "\'")
        driver.execute_script("document.getElementsByName('pw')[0].value=\'" + pw + "\'")

        driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
        driver.implicitly_wait(3)

        # driver.find_element_by_xpath('//a[@id="mail_count_profile"]/i').send_keys(Keys.ENTER)
        elem = driver.find_element_by_xpath('//a[@id="mail_count_profile"]/i')
        driver.execute_script("arguments[0].click();", elem)

        driver.find_element_by_xpath('//*[@name="frmNIDLogin"]/fieldset/span[2]/a').click()


if __name__ == "__main__":
    id = 'innotax14'
    pw = 'YDI102030**'
    # id = 'taxkmj'
    # pw = 'ekthfqksvh'
    naver = NaverLogin(id, pw)

