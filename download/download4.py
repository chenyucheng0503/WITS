from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import sys


def login_wits(driver):
    try:
        driver.get(u'https://wits.worldbank.org/WITS/WITS/Restricted/Login.aspx')
    except:
        driver.get(u'https://wits.worldbank.org/WITS/WITS/Restricted/Login.aspx')
    # login
    try:
        driver.find_element_by_id('UserNameTextBox').send_keys('zhaokui2015@hust.edu.cn')
        driver.find_element_by_id('UserPassTextBox').send_keys('GHjk&2&35')
        driver.find_element_by_id('btnSubmit').click()
    except NoSuchElementException:
        driver.get(u'https://wits.worldbank.org/WITS/WITS/Restricted/Login.aspx')
        driver.find_element_by_id('UserNameTextBox').send_keys('zhaokui2015@hust.edu.cn')
        driver.find_element_by_id('UserPassTextBox').send_keys('GHjk&2&35')
        driver.find_element_by_id('btnSubmit').click()


def restart():
    py = sys.executable
    os.execl(py, py, * sys.argv)
    print("检测到异常退出，重启程序")



def download_start():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(chrome_options=options)
    current_path = os.getcwd()
    success_path = current_path + "/successlog/success_download.txt"
    login_wits(driver)
    start_download(driver, success_path)
    driver.quit()
    restart()


download_start()