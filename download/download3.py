from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os


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


def start_download(driver, success_log):
    try:
        # 将已经完成的写入success_log
        f = open(success_log, 'a')

        # 选择第一个data
        if_exist = 1
        while if_exist == 1:
            if_success = 1

            # 重定位网站
            driver.get(u'http://wits.worldbank.org/WITS/WITS/Results/QueryView/QueryView.aspx?Page=DownloadandViewResults')

            # 选择下载
            try:
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//li[@class="rtsLI rtsLast"]/a[@class="rtsLink rtsAfter"]')))
                driver.find_element_by_xpath('//li[@class="rtsLI rtsLast"]/a[@class="rtsLink rtsAfter"]').click()
            except TimeoutException:
                if_success = 0
                print("Error: start download time out!")

            try:
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//table[@id="MainContent_QueryViewControl1_GridViewDownldList"]/tbody/tr[2]')))
            except TimeoutException:
                if_exist = 0
                print("not found!!!")
                return 0

            Query_name = driver.find_element_by_xpath('//table[@id="MainContent_QueryViewControl1_GridViewDownldList"]/tbody/tr[2]/td[2]').text

            # 点击保存
            try:
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//table[@id="MainContent_QueryViewControl1_GridViewDownldList"]/tbody/tr[2]/td[3]/a[@title="Save"]')))
                driver.find_element_by_xpath('//*[@id="MainContent_QueryViewControl1_GridViewDownldList"]/tbody/tr[2]/td[3]/a[@title="Save"]').click()
                time.sleep(10)
            except TimeoutException:
                if_success = 0
                print("保存错误")

            # 点击删除
            try:
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="MainContent_QueryViewControl1_GridViewDownldList"]/tbody/tr[2]/td[4]/a[@title="Delete"]')))
                driver.find_element_by_xpath('//*[@id="MainContent_QueryViewControl1_GridViewDownldList"]/tbody/tr[2]/td[4]/a[@title="Delete"]').click()
            except TimeoutException:
                if_success = 0
                print("删除超时")

            # 处理弹窗
            try:
                WebDriverWait(driver, 30).until(EC.alert_is_present())
                # 留一定时间来弹出弹窗，否则容易找不到
                time.sleep(1)
                try:
                    driver.switch_to.alert.accept()
                except UnexpectedAlertPresentException:
                    if_success = 0
                    print("alter error")
            except TimeoutException:
                if_success = 0
                print("alter time out ")
            time.sleep(10)

            if if_success == 1:
                f.write("success download " + Query_name + "\n")
                print("finish " + Query_name)

        f.close()
    except:
        print("unknown error!")


def download_start():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(chrome_options=options)
    current_path = os.getcwd()
    success_path = current_path + "/successlog/success_download.txt"
    login_wits(driver)
    start_download(driver, success_path)
    driver.quit()


download_start()