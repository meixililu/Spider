# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import leancloud
from leancloud import Object
from leancloud import Query
import time

leancloud.init('3fg5ql3r45i3apx2is4j9on5q5rf6kapxce51t5bc0ffw2y4', 'twhlgs6nvdt7z7sfaw76ujbmaw7l12gb8v6sdyjw1nzk9b1a')
item_id = 0

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

def get_lastest_item_id():
    query = Query('Reading')
    query.descending("item_id")
    query.limit(1)
    querys = query.find()
    if len(querys) == 0:
        return 0
    else:
        return querys[0].get("item_id")

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
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url,headers=headers)
    req.encoding='gbk'
    soup = BeautifulSoup(req.text,"html5lib")
    # print(soup)

    title = soup.find("h1", class_="ph").text

    if is_exit(title):
        print('already exit')
        return
    else:
        en = soup.find("div", id="en").text
        zh = soup.find("div", id="cn").text
        contents = en + '\n' + zh
        type_name = get_type_name(typeId)
        print(title)
        print(contents)
        print('img_url:'+img_url)
        print(typeId)
        print(type_name)
        item_id += 1
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

def get_all_link(url,catid):
    global item_id
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url,headers=headers)
    req.encoding='gbk'
    soup = BeautifulSoup(req.text,"html5lib")
    ulstr = soup.find_all(class_='f18')

    for a in ulstr:
        href = a['href']
        print('catch url:'+href)
        nowplaying_movies(href,catid)


def task():
    global item_id
    item_id = get_lastest_item_id();
    print('task start %d' % item_id)
    # catid = (1,2,3,4,8,9)
    # for i in catid:
    #     print(i)
    catid = 1
    for i in range(687,10,-1):
        url = 'http://www.hjenglish.com/fanyi/shuangyu/'
        print(url)
        get_all_link(url,catid)

def timer(n):
    while True:
        print time.strftime('%Y-%m-%d %X',time.localtime())
        task()
        time.sleep(n)

if __name__ == '__main__':
    # timer(60*60*10)
    # timer(60*60*10)
    task()




