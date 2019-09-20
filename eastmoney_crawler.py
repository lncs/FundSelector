# Author :  lncs
# Time:     2019-09-19 15:43
# File :    eastmoney_crawler.py 
# Software: PyCharm

import requests
from selenium import webdriver
import re
import pandas as pd
import pymysql


def get_page_info(url):
    options = webdriver.ChromeOptions
    prefs = {'profile.default_content_settings.popups': 0,
             "profile.default_content_setting_values.automatic_downloads": 1}
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    pass


if __name__ == '__main__':
    url = "http://cn.morningstar.com/fundselect/default.aspx"
    get_page_info(url)
