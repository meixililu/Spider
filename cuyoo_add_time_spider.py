# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import leancloud
from leancloud import Object
from leancloud import Query
import time
from selenium import webdriver
import pickle
import re
import string
from datetime import *
leancloud.init('3fg5ql3r45i3apx2is4j9on5q5rf6kapxce51t5bc0ffw2y4', 'twhlgs6nvdt7z7sfaw76ujbmaw7l12gb8v6sdyjw1nzk9b1a')
item_id = 5579

def get_type_name(type_id):
    if type_id == 1:
        return '中国'
    elif type_id == 2:
        return '国际'
    elif type_id == 3:
        return '财经'
    elif type_id == 4:
        return '科技'
    elif type_id == 8:
        return '生活'
    elif type_id == 9:
        return '社会'

def is_exit(str):
    query = Query('Reading')
    query.equal_to('title', str)
    querys = query.find()
    return len(querys) > 0

def nowplaying_movies(url,typeId):
    global item_id
    contents = ''
    img_url = ''
    type_name = ''
    browser = webdriver.PhantomJS(executable_path='/Users/luli/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs')
    browser.get(url)
    time.sleep(3)

    try:
        title = browser.find_element_by_css_selector('h1.ph').text

        if is_exit(title):
            print('already exit')
            return
        else:
            soup = BeautifulSoup(browser.page_source,"html5lib")
            wholeLayer = soup.find('div',id='wholeLayer').find_all('td',attrs={"align": "left"})
            contents = ''
            if len(wholeLayer) <= 0:
                return

            for td in wholeLayer:
                contents += td.text + '\n\n'

            type_name = get_type_name(typeId)
            print(title)
            print(contents)
            print('img_url:'+img_url)
            print(typeId)
            print(type_name)
            item_id -= 1
            Composition = Object.extend('Reading')
            mComposition = Composition()
            mComposition.set('item_id', item_id)
            mComposition.set('title', title)
            mComposition.set('img_url', img_url)
            mComposition.set('img_type', 'url')
            mComposition.set('content', contents)
            mComposition.set('type_name', type_name)
            mComposition.set('type_id', str(typeId))
            mComposition.set('source_url', url)
            mComposition.set('source_name', '酷悠双语网')
            mComposition.save()
            print('save item')
    except:
        print 'except return'
        time.sleep(5)
        return

    browser.quit()

def get_all_link(url,catid):
    global item_id
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url,headers=headers)
    req.encoding='gbk'
    soup = BeautifulSoup(req.text,"html5lib")
    ulstr = soup.find_all(class_='f18')
    time_span = soup.find_all(class_='xg1 time')

    size = len(ulstr)
    for i in range(0,size):
        href = ulstr[i]['href']
        time_str = time_span[i].text+':00'.lstrip()
        publish_time = datetime.strptime(time_str.lstrip(), "%Y-%m-%d %H:%M:%S")
        print ulstr[i].text
        print('catch url:'+href)
        print publish_time
        query = Query('Reading')
        query.contains('title', ulstr[i].text)
        querys = query.find()
        if len(querys) > 0:
            data = querys[0]
            data.set('publish_time',publish_time)
            data.save()
            print 'save publish time succee'




def task():
    # catid = (1,2,3,4,8,9)
    # for i in catid:
    #     print(i)
    catid = 1
    file1 = open(r'cuyoo_index.txt')
    index = pickle.load(file1)
    file1.close()
    for i in range(index,10):
        file = open('cuyoo_index.txt','wb')
        pickle.dump(i, file)
        file.close()
        url = 'http://www.cuyoo.com/portal.php?mod=list&catid=%d&page=%d' % (catid,i)
        print(url)
        get_all_link(url,catid)

if __name__ == '__main__':
    task()




