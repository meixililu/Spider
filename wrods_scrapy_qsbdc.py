#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import leancloud
from leancloud import Object
from leancloud import Query
from datetime import *
import time
from http_util import *
import traceback

leancloud.init('3fg5ql3r45i3apx2is4j9on5q5rf6kapxce51t5bc0ffw2y4', 'twhlgs6nvdt7z7sfaw76ujbmaw7l12gb8v6sdyjw1nzk9b1a')







# def get_item(url):
    # headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    # req = requests.get(url,headers=headers)
    # req.encoding='utf-8'
    # soup = BeautifulSoup(req.text,"html5lib")
    # alinks = soup.find_all('a', class_='n nolink')
    # for link in alinks:
    #     type_code = getType(link.text.strip())
    #     print link.text.strip()
    #     print category
    #     print type_code
    #     item_links = link.find_next_sibling().find_all('a')
    #     for item in item_links:
    #         print item.text
            # if item.text == 'meet':
            #     isStart = True
            # if isStart:
            # parseDetailPage('http://www.hujiang.com' + item['href'],item.text)






def get_urls():
    #轻松背单词
    url = 'http://word.qsbdc.com/###'
    soup = get_data_normal(url)
    contentdiv = soup.find('div',class_='index_r f_r r_bian')
    table_tr = contentdiv.find_all('tr')
    for tr in table_tr:
        tds = tr.find_all('td')
        for td in tds:
            alink = td.find('a')
            print alink.text
            if alink.text == u'列表学习':
                get_items(alink['href'])

def get_items(url):
    print url
    soup = get_data_normal(url)
    table = soup.find('div',class_='index_r f_r r_bian').find('table', class_='table_solid')
    trs = table.find_all('tr')
    page_tr = trs[len(trs)-1]
    next_num = page_tr.find_all('option')
    next_pages = page_tr.find_all('a')
    for tr in trs:
        print tr.text


    


    # for link in next_pages:
    #     if u'下一页' in link.text:
    #         get_items(url[:url.index('?')] + link['href'])



if __name__ == '__main__':
    # get_item('http://www.hujiang.com/ciku/zuixinyingyusijicihui/')
    # get_urls()
    get_items('http://word.qsbdc.com/wl.php?level=1')