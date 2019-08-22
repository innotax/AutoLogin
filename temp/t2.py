from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

cap = DesiredCapabilities().INTERNETEXPLORER
# cap['platform'] = "Win8"
cap['platform'] = "windows"
cap['version'] = "11"
cap['browserName'] = "internet explorer"
cap['ignoreProtectedModeSettings'] = True
cap['nativeEvents'] = False
cap['requireWindowFocus'] = True
cap['INTRODUCE_FLAKINESS_BY_IGNORING_SECURITY_DOMAINS'] = True
driver=webdriver.Ie(capabilities=cap, executable_path=r'C:\zz\NTS\driver\IEDriverServer.exe')

driver.get("https://www.facebook.com/")