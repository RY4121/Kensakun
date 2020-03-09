# -*- coding: utf-8 -*-
import traceback
import requests
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
from datetime import datetime


class Time:

    def __init__(self, base_url):
        self.base_url = base_url

    def getData(self, type):
        request = req.urlopen(self.base_url)
        soup = BeautifulSoup(request, "html.parser")

        time_list = []
        hour_list = []
        minute_list = []

        # 情報のスクレイピング
        if type == 1 or type == 2:
            table = soup.find_all('table')[0]
        elif type == 3 or type == 4:
            table = soup.find_all('table')[1]

        for tags in table.find_all('tr'):
            for value in tags.find_all('td'):
                if 'キャンパス' in value:
                    pass
                else:
                    time_list.append(value.text)

        if type == 1:
            time_list = time_list[1::4]
        elif type == 2:
            time_list = time_list[0::4]
        elif type == 3:
            time_list = time_list[1::4]
        elif type == 4:
            time_list = time_list[0::4]

        print('time_list::', time_list)
        # 時間と分に分けて格納
        for x in time_list:
            if x != '':
                hour_list.append(x.split(':')[0])
                minute_list.append(x.split(':')[1])

        # 2桁のうち0を排除
        for x, y in zip(hour_list, minute_list):
            if x.split('0')[0] == '':
                if x.split('0')[1] == '':
                    hour_list[hour_list.index(x)] = '00'
                else:
                    hour_list[hour_list.index(x)] = '0' + x.split('0')[1]
            if y.split('0')[0] == '':
                if y.split('0')[1] == '':
                    minute_list[minute_list.index(y)] = '00'
                else:
                    minute_list[minute_list.index(y)] = '0' + y.split('0')[1]

        try:
            now = datetime.today()

            now = datetime(2015, 1, 1, 12, 30, 59, 0)
            TIME_WIDTH = 5
            hour_index = hour_list.index(str(now.hour))
            h_t = hour_list[hour_index:hour_index + TIME_WIDTH]
            m_t = minute_list[hour_index:hour_index + TIME_WIDTH]
            print('MINUTE_TIME', m_t)
            time_info = []
            for x, y in zip(h_t, m_t):
                time_info.append(x + ':' + y)
            # print(time_info)
            return time_info
        except ValueError:
            print('今日のバスの運行はありません')
            return '今日のバスの運行はありません'


if __name__ == '__main__':
    OBJECT_URL = 'https://www.teu.ac.jp//campus/access/2020_0307_0314_bus.html'
    time = Time(OBJECT_URL)
    print(time.getData(3))
