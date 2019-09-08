from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
import os

chrome_path = r"C:\Ataxtech\AutoLogin\loginAPP\driver\chromedriver"
# chrome_option = Options()
# chrome_option.add_argument("--headless")
# chrome_option.add_argument("--window-size=1920*1080")
# chrome_option.add_argument("disable-gpu")
# chrome_option.add_argument("""user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4)
#      AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36""")

# chrome_option.binary_location= r"C:\Users\taxkm\AppData\Local\Google\Chrome\User Data\PepperFlash\32.0.0.238\pepflashplayer.dll"
# driver = webdriver.Chrome(executable_path=chrome_path,
#                             chrome_options=chrome_option)
# driver.execute_script("Object.defineProperty(navigator, 'languages', 
#                       {get: function() {return ['ko-KR', 'ko']})")
# driver.execute_script("Object.defineProperty(navigator, 'plugins', 
#                       {get: function() {return[1, 2, 3, 4, 5]}})")


# 크롬 headless 모드 실행
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('lang=ko_KR')

driver = webdriver.Chrome(chrome_path, chrome_options=chrome_options)
driver.implicitly_wait(3)

driver.get('https://developer-ankiwoong.tistory.com/60')