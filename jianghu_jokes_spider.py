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
import re
import types
import traceback

leancloud.init('3fg5ql3r45i3apx2is4j9on5q5rf6kapxce51t5bc0ffw2y4', 'twhlgs6nvdt7z7sfaw76ujbmaw7l12gb8v6sdyjw1nzk9b1a')

def nowplaying_movies(url,img_url):
    # url = 'http://news.iciba.com/study/bilingual/1538012.shtml'
    global source_name
    global category
    global type
    global item_id
    global category_2
    global type_name
    contents = ''
    media_url = ''
    publish_time = ''
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url,headers=headers)
    req.encoding='utf-8'
    soup = BeautifulSoup(req.text,"html5lib")

    try:
        title = soup.find('h1',id='article_title').text
        if u'外语角' in title or u'移动学习' in title or u'视频' in title or u'出国留学你我都会遭遇' in title:
            print 'title has 外语角'
            return
        if is_exit(title):
            print('already exit')
            return
        else:
            div = soup.find('div',id='article')
            if div is None:
                print 'content is none,div == none, return'
                return

            img = div.find('img')
            if img is not None:
                img_url = img['src']

            publish_time = datetime.now()

            for con in div.get_text().splitlines():
                if con is None:
                    pass
                elif u'HJPlayer' in  con or u'更多内容' in con or u'请勿转载' in con or u'09年雅思考试' in con or u'新东方' in con or u'公开课' in con or u'推荐' in con or u'别再错过' in con:
                    pass
                elif u'未能参与现场' in  con or u'想参与' in con or u'【新东方在线】' in con or u'您的浏览器' in con or u'求关注' in con or 'ijinshanciba' in con or u'帐号：' in con or u'号外号外' in con:
                    pass
                elif u'金山词霸微信版开通啦' in  con or u'点击进入' in con or u'专为' in con or u'您的浏览器' in con or u'求关注' in con or 'ijinshanciba' in con or u'帐号：' in con or u'号外号外' in con:
                    pass
                elif len(con) == 0:
                    pass
                else:
                    contents += con.strip()
                    contents += '\n\n'
            contents = contents.strip()

            if contents == '':
                print('contents is empty, return')
                return


            mp3div = soup.find('source')
            if mp3div is not None:
                type = 'mp3'
                media_url = mp3div['src']
            else:
                type = 'text'

            item_id += 1
            typeId = get_type_id(type_name)
            print title
            print item_id
            print typeId
            print type_name
            print media_url
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
            mComposition.set('category_2', category_2)
            mComposition.set('type', type)
            mComposition.set('media_url', media_url)
            mComposition.save()
            print('save item')
    except:
        print traceback.format_exc()
        print url
        return

def get_type_id(type_name):
    return '1012'

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
    req.encoding='utf-8'
    soup = BeautifulSoup(req.text,"html5lib")
    div = soup.find('div', class_='main-cntlst m-atc-lst m-atc-img-lst md0 mdc0 show')
    ulstr = div.find_all('a')
    for i in range(len(ulstr)-1,-1,-1):
        href = ulstr[i]['href']
        print 'catch url:' + href
        nowplaying_movies(href,'')

item_id = 0
source_name = '沪江英语'
category = 'jokes'
category_2 = ''
type = 'text'
type_name = '英语笑话大全'

def task():
    global item_id
    global category
    global category_2
    global type_name
    item_id = get_lastest_item_id();
    print('item_id %d' % item_id)
    index = 0
    type0 = [('yingyuxiaohuadaquan',16)]
    type1 = [('take_away_english',2),('todays_phrase',3),('story_of_the_week',2),('q_and_a',2),('media_english',2),('bbc_quiz',2)]
    type2 = [('quwen',11),('meiju',3),('dianying',2),('lvyou',43),('shishang',40)]

    for index in range(0,3):
        if index == 0:
            type_name = '英语笑话大全'
            type = type0
        elif index == 1:
            type_name = 'bbc英语'
            type = type1
        elif index == 2:
            type_name = '双语阅读'
            type = type2


        for item in type:
            for i in range(1,2):
            # for i in range(item[1],0,-1):
                if index == 0:
                    category = 'jokes'
                elif index == 1:
                    category = 'shuangyu_reading'
                elif index == 2:
                    category = 'shuangyu_reading'
                if i == 1:
                    url = 'http://www.hjenglish.com/yingyuxiaohua/%s/' % (item[0])
                else:
                    url = 'http://www.hjenglish.com/yingyuxiaohua/%s_%d/'% (item[0],i)
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




