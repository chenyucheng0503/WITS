from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import traceback


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
            time.sleep(1)
        except TimeoutException:
            print("nomenclature_select time out " + HS_Code + "_" + year + "_" + flow)
            f.write("Error: nomenclature_select time out " + HS_Code + "_" + year + "_" + flow + "\n")
            return 0

        """Year Select"""
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

        """ Flow Select """
        try:
            time.sleep(0.5)
            WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.ID, 'MainContent_drdFlow'))
            )
            flow_select = Select(driver.find_element_by_xpath('//*[@id="MainContent_drdFlow"]'))
            flow_list = ['Gross Imports', 'Gross Exports', 'Re-Exports', 'Re-Imports']
            flow_select.select_by_visible_text(flow_list[int(flow) - 1])
        except TimeoutException:
            print("flow_select time out " + HS_Code + "_" + year + "_" + flow)
            f.write("Error: flow_select time out " + HS_Code + "_" + year + "_" + flow + "\n")
            return 0

        """ Tier select """
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'MainContent_drdTier'))
            )
            tier_select = Select(driver.find_element_by_id('MainContent_drdTier'))
            tier_select.select_by_value("3")
            time.sleep(1)
        except TimeoutException:
            print("tier_select time out " + HS_Code + "_" + year + "_" + flow)
            f.write("Error: tier_select time out " + HS_Code + "_" + year + "_" + flow + "\n")
            return 0

        """HS_Code select"""
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

        """Reporter"""
        time.sleep(0.5)
        is_reporter_clickable = driver.find_element_by_id('btnReporterSelectAll').is_enabled()
        if is_reporter_clickable:
            driver.find_element_by_id('btnReporterSelectAll').click()
        else:
            print("Cannot reporter " + HS_Code + "_" + year + "_" + flow)
            f.write("Error:Cannot reporter " + HS_Code + "_" + year + "_" + flow + "\n")
            return 0

        """Partner"""
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

        """Download Report"""
        try:
            WebDriverWait(driver, 20).until(
                EC.frame_to_be_available_and_switch_to_it('rptdownloadreport')
            )
        except TimeoutException:
            print("frame time out " + HS_Code + "_" + year + "_" + flow)
            f.write("Error:frame time out " + HS_Code + "_" + year + "_" + flow + "\n")
            return 0

        """ Job Name & Describe """
        job_name = HS_Code + "to" + year + "to" + flow
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "RptCoulmnSelection1_txtJobDescription"))
            )
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'RptCoulmnSelection1_txtJobName'))
            )
            driver.find_element_by_id('RptCoulmnSelection1_txtJobName').send_keys(job_name)
            # print("名字OK")
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'RptCoulmnSelection1_txtJobDescription'))
            )
            driver.find_element_by_id('RptCoulmnSelection1_txtJobDescription').send_keys(job_name)
            # print("描述OK")
        except TimeoutException:
            print("job name time out " + HS_Code + "_" + year + "_" + flow)
            f.write("Error: job name time out " + HS_Code + "_" + year + "_" + flow + "\n")
            return 0

        """ Download Click """
        try:
            time.sleep(10)
            # print("开始下载")
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'RptCoulmnSelection1_btnProcessed'))
            )
            download_element = driver.find_element_by_id('RptCoulmnSelection1_btnProcessed')
            # print("找到元素")
            ActionChains(driver).click(download_element).perform()
            # print("点击元素")
            # ActionChains(driver).move_to_element(download_element).click(download_element).perform()
        except TimeoutException:
            print("download time out " + HS_Code + "_" + year + "_" + flow)
            f.write("Error: download time out " + HS_Code + "_" + year + "_" + flow + "\n")
            return 0

        """ Alert Dismiss"""
        try:
            WebDriverWait(driver, 60).until(
                EC.alert_is_present()
            )
            # 留一定时间来弹出弹窗，否则容易找不到
            time.sleep(1)
            try:
                driver.switch_to.alert.dismiss()
            except UnexpectedAlertPresentException:
                print("alter2 time out " + HS_Code + "_" + year + "_" + flow)
                f.write("Warning:alter time out " + HS_Code + "_" + year + "_" + flow + "\n")
                return 0
        except TimeoutException:
            print("alter1 time out " + HS_Code + "_" + year + "_" + flow)
            f.write("Warning:alter time out " + HS_Code + "_" + year + "_" + flow + "\n")
            return 0

        print("finish " + HS_Code + "_" + year + "_" + flow + ", Time Cost " + str(time.time()-start_time) + "s!")
        # 写入成功文件
        f_success.write(HS_Code + "_" + year + "_" + flow + "\n")
        f.close()
        time.sleep(1)
        return 1
    except Exception as e:
        print(e)
        print("unknown error:" + HS_Code + "_" + year + "_" + flow)
        f.write("Error: unknown error " + HS_Code + "_" + year + "_" + flow + "\n")
        return 0


def CSV_start(csv_path, error_log, success_log, line_log):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        prefs = {'profile.default_content_setting_values.automatic_downloads': 1,
                 'profile.default_content_settings.popups': 0}
        options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(options=options)
        login_wits(driver)

        csv_count = len(open(csv_path, 'r').readlines())
        curr_f = open(line_log, 'r')
        current_line = int(curr_f.read())
        global x
        x = 0
        with open(csv_path, 'r') as f:
            for i in range(csv_count):
                if i < current_line:
                    f.readline()
                    continue
                else:
                    csv_str = f.readline()
                    hs_code = csv_str.split(',')[1].zfill(6)
                    year = csv_str.split(',')[2]
                    flow = csv_str.split(',')[3]
                    start_wits(driver, year, flow, hs_code, error_log, success_log)
                x += 1
        driver.quit()
    except:
        f = open(line_log, 'w')
        f.write((str(x)))
        print("Unknown Error！当前line为" + str(x))
        traceback.print_exc()
        f.close()


