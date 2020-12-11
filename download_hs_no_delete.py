import traceback

import selenium
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
    except Exception:
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


def start_download(driver, success_log, page_log):
    try:
        """
        重定位网站
        """
        driver.get(u'http://wits.worldbank.org/WITS/WITS/Results/QueryView/QueryView.aspx?Page=DownloadandViewResults&Download=true')


        """
        跳转到第 Page 页
        """
        f = open(page_log, 'r')
        page = int(f.read())

        # 发送js命令
        driver.execute_script("__doPostBack('ctl00$MainContent$QueryViewControl1$GridViewDownldList','Page$" + str(page) + "')")
        time.sleep(10)

        """
        点击保存
        """
        while True:
            if_success = 1

            for i in range(2, 22):
                Query_name = driver.find_element_by_xpath('//table[@id="MainContent_QueryViewControl1_GridViewDownldList"]/tbody/tr[' + str(i) + ']/td[2]').text
                node_number = driver.find_element_by_xpath('//table[@id="MainContent_QueryViewControl1_GridViewDownldList"]/tbody/tr[' + str(i) + ']/td[1]').text
                # 点击保存
                try:
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//table[@id="MainContent_QueryViewControl1_GridViewDownldList"]/tbody/tr[' + str(i) + ']/td[3]/a[@title="Save"]')))
                    driver.find_element_by_xpath('//*[@id="MainContent_QueryViewControl1_GridViewDownldList"]/tbody/tr[' + str(i) + ']/td[3]/a[@title="Save"]').click()
                    time.sleep(1)
                except Exception:
                    if_success = 0

                    # 是否 Abort
                    abort = driver.find_element_by_xpath('//table[@id="MainContent_QueryViewControl1_GridViewDownldList"]/tbody/tr[' + str(i) + ']/td[5]/input')
                    if_abort = bool(abort.get_attribute("src") == "http://wits.worldbank.org/WITS/WITS/images/Aborted.bmp")
                    print(if_abort)

                    if if_abort:
                        continue

                    # 保存当前 Page 页
                    f = open(page_log, 'w')
                    f.write(str(page))
                    print("保存错误，当前page为" + (str(page)))
                    f.close()
                    return 0

                if if_success == 1:
                    # 将已经完成的写入success_log
                    f = open(success_log, 'a')
                    f.write("success download " + Query_name + "\n")
                    print("finish " + node_number + " : " + Query_name)
                    f.close()

            """
            转到下一页,同时page+1
            """
            driver.execute_script("__doPostBack('ctl00$MainContent$QueryViewControl1$GridViewDownldList','Page$" + str(page+1) + "')")
            try:
                WebDriverWait(driver, 30).until_not(EC.text_to_be_present_in_element((By.XPATH, '//table[@id="MainContent_QueryViewControl1_GridViewDownldList"]/tbody/tr[last()-1]/td[2]'), Query_name))
                page += 1
            except TimeoutException:
                driver.execute_script("__doPostBack('ctl00$MainContent$QueryViewControl1$GridViewDownldList','Page$" + str(page + 1) + "')")
                WebDriverWait(driver, 30).until_not(EC.text_to_be_present_in_element((By.XPATH, '//table[@id="MainContent_QueryViewControl1_GridViewDownldList"]/tbody/tr[last()-1]/td[2]'), Query_name))
                page += 1

    except selenium.common.exceptions.UnexpectedAlertPresentException:
        f = open(page_log, 'w')
        f.write((str(page)))
        print("UnexpectedAlertPresentException！当前page为" + str(page))
        f.close()
    except:
        f = open(page_log, 'w')
        f.write((str(page)))
        print("Unknown Error！当前page为" + str(page))
        traceback.print_exc()
        f.close()


def download_start():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    prefs = {'profile.default_content_setting_values.automatic_downloads': 1,
             'profile.default_content_settings.popups': 0}
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=options)
    current_path = os.getcwd()
    success_path = current_path + "/success_download.txt"
    page_log = current_path + "/page_log.txt"
    login_wits(driver)
    start_download(driver, success_path, page_log)
    driver.quit()


download_start()
