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

leancloud.init('3fg5ql3r45i3apx2is4j9on5q5rf6kapxce51t5bc0ffw2y4', 'twhlgs6nvdt7z7sfaw76ujbmaw7l12gb8v6sdyjw1nzk9b1a')

def nowplaying_movies(url,publish_time):
    global source_name
    global category
    global type
    global item_id
    contents = ''
    type_name = ''
    img_url = ''
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url,headers=headers)
    req.encoding='gbk'
    soup = BeautifulSoup(req.text,"html5lib")

    div = soup.find('div',class_='details_main1_left_content')
    if div == None:
        print('div == none, return')
        return

    size = len(div.find_all('p'))
    if size > 0:
        for i in range(0,size):
            con = div.find_all('p')[i].text
            if len(con) > 0:
                if u'相关推荐' in  con or u'返回专题' in con or u'儿童英语小短文汇总文章导航' in con or u'/*页面中表格样式*/' in con or u'好听的英文儿童歌曲大全文章导航' in con or u'阅读排行' in con:
                    print 'con has 相关推荐 or 返回专题 or 儿童英语小短文汇总文章导航'
                    break
                elif u'英语网整理' in con:
                    print 'con has 英语网整理'
                    pass
                else:
                    tem = con.lstrip()
                    contents += tem
                    contents += '\n'
    else:
        print('content size = 0, return')
        return

    if contents.strip() == '':
        content_divs = div.select('div div div')
        # print content_divs
        for cd in content_divs:
            contents += cd.text.lstrip()
            contents += '\n'

    if contents.strip() == '':
        content_divs = div.select('div div')
        # print content_divs
        for cd in content_divs:
            contents += cd.text.lstrip()
            contents += '\n'

    if contents.strip() == '':
        print('contents is empty, return')
        return


    title = soup.find('h1',class_='details_main1_left_title').text
    type_name = '少儿英语故事'
    if is_exit(title):
        print('already exit')
        return
    else:
        item_id += 1
        typeId = get_type_id(type_name)
        print title
        print item_id
        print typeId
        print type_name
        print img_url
        print publish_time
        print ('contents:\n' + contents)

        Composition = Object.extend('Reading')
        mComposition = Composition()
        mComposition.set('item_id', item_id)
        mComposition.set('title', title)
        mComposition.set('img_url', img_url)
        mComposition.set('img_type', 'url')
        mComposition.set('content', contents)
        mComposition.set('type_name', type_name)
        mComposition.set('publish_time', publish_time)
        mComposition.set('type_id', typeId)
        mComposition.set('source_url', url)
        mComposition.set('source_name', source_name)
        mComposition.set('category', category)
        mComposition.set('type', type)
        mComposition.save()
        print('save item')

def get_type_id(type_name):
    return '1008'

def is_exit(str):
    global category
    query = Query('Reading')
    query.equal_to('title', str)
    query.equal_to('category', category)
    querys = query.find()
    return len(querys) > 0

def get_lastest_item_id():
    global source_name
    global category
    query = Query('Reading')
    query.equal_to('category', category)
    query.equal_to('source_name', source_name)
    query.descending("item_id")
    query.limit(1)
    querys = query.find()
    if len(querys) == 0:
        return 0
    else:
        return querys[0].get("item_id")

def get_all_link(url):
    global item_id
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url,headers=headers)
    req.encoding='gbk'
    soup = BeautifulSoup(req.text,"html5lib")
    ulstr = soup.find_all('span',class_='list_main1_tuijian_content')
    dates = soup.find_all('span', class_='list_main1_tuijian_time')
    for i in range(0,len(ulstr)):
        href = ulstr[i].find('a')['href']
        datestr = dates[i].find('a').text
        publish_time = datetime.strptime(datestr.lstrip(), "%Y-%m-%d")
        print('catch url:' + href)
        nowplaying_movies(href,publish_time)

item_id = 0
source_name = '英语网'
category = 'story'
type = 'text'

def task():
    global item_id
    item_id = get_lastest_item_id();
    print('task start %d' % item_id)
    for i in range(1,2):
        if i == 1:
            url = 'http://www.yingyu.com/seyy/gushi/index.shtml'
        else:
            url = 'http://www.yingyu.com/seyy/gushi/index_%d.shtml'% (i)
        print('root url:'+url)
        get_all_link(url)

def timer(n):
    while True:
        print time.strftime('%Y-%m-%d %X',time.localtime())
        task()
        time.sleep(n)

if __name__ == '__main__':
    # timer(60*60*10)
    # timer(60*60*10)
    task()




