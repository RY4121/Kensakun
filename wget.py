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


def form_submit(base_url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    html_list = []
    try:
        driver.get(base_url)
        time.sleep(2)
        word = driver.find_element_by_id('naviapi-search-text')
        word.send_keys(search_word)
        time.sleep(2)
        html_list.append(driver.page_source)

        driver.quit()
    except:
        driver.quit()

    return html_list


def getStoreInfo(search_word):
    base_url = 'https://www.dmm.co.jp/top/'
    soup = BeautifulSoup(requests.get(base_url).content, "html.parser")

    form_submit(base_url, search_word)


# 実行用
if __name__ == "__main__":

    Yahoo.getStoreInfo()
