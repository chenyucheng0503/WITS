# coding=utf-8

"""
Author:Graham
data: 2020/12/10 9:26
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

driver.get('http://www.python.org')
element = driver.find_element_by_xpath('//*[@id="submit"]')
print("type:", element.get_attribute("type"))

