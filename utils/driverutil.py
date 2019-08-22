import os, sys, time, json, zipfile

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))                                   # 1단계 상위폴더
from utils import Util

def get_element(driver, id):
    try:
        if "세무법인이노택스테헤" not in id:
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.presence_of_element_located((By.XPATH, f"//*[@id=\'{id}\']")))
        elif "세무법인이노택스테헤" in id:
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.presence_of_element_located((By.XPATH, f"//*[@title=\'{id}\']")))
        return element

    except Exception as e:
        err_class_name = e.__class__.__name__
        msg = f"selenium id < {id} >에서 예외 < {err_class_name} >가 발생 하였습니다."
        errmsg = Util.Errpop().critical_pop(msg)

class Get_driver():
    def __init__(self, driver_path, driver_name):
        self.driver_path = driver_path
        self.driver_name = driver_name
        self.full_driver_name = os.path.join(self.driver_path, self.driver_name)

    def set_driver(self):
        
        if "chrome" in self.full_driver_name:
            
            try:
                chrome_options = webdriver.ChromeOptions()

                driver = webdriver.Chrome(self.full_driver_name, options=chrome_options)
                return driver
            except:
                msg = "드라이버 경로( {0} )에 {1}이(가) 없습니다 !!!".format(self.driver_path, self.driver_name)
                errmsg = Util.Errpop().critical_pop(msg)
                
        elif True :
            pass    

class IE_driver():
    def __init__(self, driver_path, driver_name):
        self.driver_path = driver_path
        self.driver_name = driver_name
        self.full_driver_name = os.path.join(self.driver_path, self.driver_name)

    def set_driver(self):
        print(self.full_driver_name )
        if "IEDriverServer" in self.full_driver_name:
            try:
                driver = webdriver.Ie(executable_path=self.full_driver_name)
                print('111')
                return driver
            except:
                print('222')
                msg = "드라이버 경로( {0} )에 {1}이(가) 없습니다 !!!".format(self.driver_path, self.driver_name)
                errmsg = Util.Errpop().critical_pop(msg)
                
        elif True :
            pass    


if __name__ == '__main__':

    # driver = Get_driver(r'C:\zz\NTS\driver', 'chromedriver.exe')
    driver = IE_driver(r'C:\zz\NTS\driver', 'IEDriverServer.exe')
    driver = driver.set_driver()