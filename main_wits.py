from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


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


def start_wits(driver, year, flow, HS_Code, error_log, success_log):
    try:
        start_time = time.time()            # 记录时间
        f = open(error_log, 'a')            # 将未完成的写入error_log
        f_success = open(success_log, 'a')  # 将已经完成的写入success_log

        # 重定位网站
        driver.get(u'http://wits.worldbank.org/WITS/WITS/QuickQuery/ComtradeByProduct/ComtradeByProduct.aspx?Page=COMTRADEByProduct')
        driver.find_element_by_id('btnReset').click()

        # nomenclature select
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'MainContent_drdNomenclature'))
            )
            nomenclature_select = Select(driver.find_element_by_id('MainContent_drdNomenclature'))
            nomenclature_select.select_by_value("H1  ~  1996|2019")
        except TimeoutException:
            print("nomenclature_select time out " + HS_Code + "_" + year + "_" + flow)
            f.write("Error: nomenclature_select time out " + HS_Code + "_" + year + "_" + flow + "\n")
            return 0

        # year select
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'MainContent_drdYear'))
            )
            year_select = Select(driver.find_element_by_id('MainContent_drdYear'))
            year_select.select_by_value(year)
        except TimeoutException:
            print("year_select time out " + HS_Code + "_" + year + "_" + flow)
            f.write("Error: year_select time out " + HS_Code + "_" + year + "_" + flow + "\n")
            return 0

        # flow select
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'MainContent_drdFlow'))
            )
            flow_select = Select(driver.find_element_by_id('MainContent_drdFlow'))
            flow_select.select_by_value(flow)
        except TimeoutException:
            print("flow_select time out " + HS_Code + "_" + year + "_" + flow)
            f.write("Error: flow_select time out " + HS_Code + "_" + year + "_" + flow + "\n")
            return 0

        # tier select
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'MainContent_drdTier'))
            )
            tier_select = Select(driver.find_element_by_id('MainContent_drdTier'))
            tier_select.select_by_value("3")
        except TimeoutException:
            print("tier_select time out " + HS_Code + "_" + year + "_" + flow)
            f.write("Error: tier_select time out " + HS_Code + "_" + year + "_" + flow + "\n")
            return 0

        # HS_Code select
        driver.find_element_by_id('ctl00_MainContent_drdProduct_Input').clear()
        driver.find_element_by_id('ctl00_MainContent_drdProduct_Input').send_keys(HS_Code)
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_MainContent_drdProduct_DropDown"]/div[1]/ul/li[3]'))
            )
            HS_text = driver.find_element_by_xpath('//*[@id="ctl00_MainContent_drdProduct_DropDown"]/div[1]/ul/li[3]').text
            if HS_text != "Total All products":
                driver.find_element_by_xpath('//*[@id="ctl00_MainContent_drdProduct_DropDown"]/div[1]/ul/li[3]').click()
            else:
                print("hscode not found " + HS_Code + "_" + year + "_" + flow)
                f.write("Error: hscode not found " + HS_Code + "_" + year + "_" + flow + "\n")
                return 0
        except TimeoutException:
            print("hscode_select time out " + HS_Code + "_" + year + "_" + flow)
            f.write("Error: hscode_select time out " + HS_Code + "_" + year + "_" + flow + "\n")
            return 0

        # reporter
        time.sleep(0.5)
        is_reporter_clickable = driver.find_element_by_id('btnReporterSelectAll').is_enabled()
        if is_reporter_clickable:
            driver.find_element_by_id('btnReporterSelectAll').click()
        else:
            print("Cannot reporter " + HS_Code + "_" + year + "_" + flow)
            f.write("Error:Cannot reporter " + HS_Code + "_" + year + "_" + flow + "\n")
            return 0

        # partner
        is_partner_clickable = driver.find_element_by_id('btnPartnerSelectAll').is_enabled()
        if is_partner_clickable:
            driver.find_element_by_id('btnPartnerSelectAll').click()
        else:
            print("Cannot partner " + HS_Code + "_" + year + "_" + flow)
            f.write("Error:Cannot partner " + HS_Code + "_" + year + "_" + flow + "\n")
            return 0

        # 有时候会没有reporters导致无法点击download按钮
        is_download_clickable = driver.find_element_by_id('MainContent_btnDownload').is_enabled()
        if is_download_clickable:
            driver.find_element_by_id('MainContent_btnDownload').click()
        else:
            print("Cannot download" + HS_Code + "_" + year + "_" + flow)
            f.write("Error:Cannot download " + HS_Code + "_" + year + "_" + flow + "\n")
            return 0

        # Job describe
        try:
            WebDriverWait(driver, 20).until(
                EC.frame_to_be_available_and_switch_to_it('rptdownloadreport')
            )
        except TimeoutException:
            print("frame time out " + HS_Code + "_" + year + "_" + flow)
            f.write("Error:frame time out " + HS_Code + "_" + year + "_" + flow + "\n")
            return 0

        # job name & describe
        job_name = HS_Code + "to" + year + "to" + flow
        try:
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'RptCoulmnSelection1_txtJobName'))
            )
            driver.find_element_by_id('RptCoulmnSelection1_txtJobName').send_keys(job_name)
        except TimeoutException:
            print("job name time out " + HS_Code + "_" + year + "_" + flow)
            f.write("Error: job name time out " + HS_Code + "_" + year + "_" + flow + "\n")
            return 0
        driver.find_element_by_id('RptCoulmnSelection1_txtJobDescription').send_keys(job_name)

        # download click
        try:
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'RptCoulmnSelection1_btnProcessed'))
            )
            driver.find_element_by_id('RptCoulmnSelection1_btnProcessed').click()
        except TimeoutException:
            print("download time out " + HS_Code + "_" + year + "_" + flow)
            f.write("Error: download time out " + HS_Code + "_" + year + "_" + flow + "\n")
            return 0

        # alert dismiss
        try:
            WebDriverWait(driver, 20).until(
                EC.alert_is_present()
            )
            # 留一定时间来弹出弹窗，否则容易找不到
            time.sleep(1)
            try:
                driver.switch_to.alert.dismiss()
            except UnexpectedAlertPresentException:
                print("alter time out " + HS_Code + "_" + year + "_" + flow)
                f.write("Warning:alter time out " + HS_Code + "_" + year + "_" + flow + "\n")
                return 0
        except TimeoutException:
            print("alter time out " + HS_Code + "_" + year + "_" + flow)
            f.write("Warning:alter time out " + HS_Code + "_" + year + "_" + flow + "\n")
            return 0

        print("finish " + HS_Code + "_" + year + "_" + flow + ", Time Cost " + str(time.time()-start_time) + "s!")
        # 写入成功文件
        f_success.write(HS_Code + "_" + year + "_" + flow + "\n")
        f.close()
        time.sleep(1)
        return 1
    except:
        print("unknown error" + HS_Code + "_" + year + "_" + flow)
        f.write("Error: unknown error " + HS_Code + "_" + year + "_" + flow + "\n")
        return 0


def HS_start(HS_Code, year, flow, error_log, success_log):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(chrome_options=options)
    login_wits(driver)
    start_wits(driver, str(year), str(flow), str(HS_Code), error_log, success_log)
    driver.quit()
