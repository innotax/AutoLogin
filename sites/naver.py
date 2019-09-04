### 네이버 로그인 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

chrome_path = r'C:\zz\NTS\driver\chromedriver.exe'
driver = webdriver.Chrome(chrome_path)
driver.implicitly_wait(3)
driver.get('https://nid.naver.com/nidlogin.login')

# driver.find_element_by_id('id').send_keys('taxkmj')
# driver.find_element_by_id('pw').send_keys('ekthfqksvh')
### 자동입력방지문자 우회 https://sab-jil.tistory.com/2
id = 'taxkmj'
pw = 'ekthfqksvh'
driver.execute_script("document.getElementsByName('id')[0].value=\'" + id + "\'")
driver.execute_script("document.getElementsByName('pw')[0].value=\'" + pw + "\'")

driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
driver.implicitly_wait(3)

# driver.find_element_by_xpath('//a[@id="mail_count_profile"]/i').send_keys(Keys.ENTER)
elem = driver.find_element_by_xpath('//a[@id="mail_count_profile"]/i')
driver.execute_script("arguments[0].click();", elem)

# 네이버 캡차(Captcha) 무력화 https://hyrama.com/?p=693