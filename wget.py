# -*- coding: utf-8 -*-
import traceback
import requests
import chromedriver_binary
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from urllib.error import URLError, HTTPError
import time
import codecs
import urllib.parse as par
import urllib.request as req
from bs4 import BeautifulSoup
import pandas as pd
import re
import ssl
import csv
import os
import sys
import pathlib
import uuid
import requests
from requests.compat import urljoin
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + '/../')

# from modules.db_util import *
# from modules.update_db import *


def form_submit(base_url, search_word):
    print('input form_submit()')
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
# https://www.dmm.co.jp/search/=/searchstr=%E5%AE%89%E9%BD%8B%E3%82%89%E3%82%89/analyze=V1ECCVYFUQc_/sort=rankprofile/
    html_list = []
    try:
        driver.get(base_url)
        time.sleep(5)
        print('url::', base_url)
        print('driver.get(base_url)')

        # word = driver.find_element_by_id('naviapi-search-text')
        # word.send_keys(search_word)
        word = driver.find_element_by_xpath('//*[@id="naviapi-search-text"]')
        word.send_keys(search_word)
        time.sleep(5)
        print('word.send_keys(search_word)')

        input = driver.find_element_by_xpath(
            '//*[@id="naviapi-search-submit"]').click()
        driver.execute_script("arguments[0].click();", input)
        time.sleep(5)
        print('ラストスパート')

        html_list.append(driver.page_source)

        driver.quit()
    except Exception as e:
        print('Error::', e)
        driver.quit()

    print('depart form_submit()')
    return html_list


def getStoreInfo(search_word):
    base_url = 'https://www.dmm.co.jp/top/'

    html_list = form_submit(base_url, search_word)

    title_list = []
    link_list = []
    error_flag = False
    em = ''
    for html in html_list:
        # print('html source::', html)
        soup = BeautifulSoup(html, "html.parser")
        ul_tag = soup.find('ul', id='list')
        for tag_1 in ul_tag.find_all('li'):
            try:
                link = tag_1.find('p', class_='tmb').a.attrs['href']
                title = tag_1.find('span', class_='txt').text
                title_list.append(title)
                link_list.append(link)
            except Exception as e:
                print('Exception::', e)
                error_flag = True
                em = str(e)
                continue

    if error_flag:
        title_list.append('何らかの理由で取得できませんでした')
        link_list.append(em)
    else:
        title_list.append('Seki')
        link_list.append('Akio')

    result_list = []
    for x, y in zip(title_list, link_list):
        result_list.append([x, y])

    print(result_list)
    return result_list


# 実行用
# if __name__ == "__main__":
#     getStoreInfo('安齋らら')
