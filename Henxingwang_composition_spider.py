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
item_id = 0

def nowplaying_movies(url,publish_time):
    global item_id
    contents = ''
    img_url = ''
    type_name = ''
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url,headers=headers)
    req.encoding='gbk'
    soup = BeautifulSoup(req.text,"html5lib")

    div = soup.find('div',id='arctext')
    if div == None:
        print(div)
        print('div == none:')
        return

    size = len(div.find_all('p'))
    if size > 0:
        image = soup.p.img
        start = 0
        if image != None:
            img_url = image.attrs["src"]
            start = 1

        for i in range(start,size):
            contents += div.find_all('p')[i].text
            contents += '\n'
    else:
        print('return')
        return

    if contents.strip() == '':
        print('contents == kong')
        return

    titles = soup.title.text.split('|')
    title_size = len(titles)
    if title_size > 1:
        title = soup.title.text.split('|')[0]
        type_name = soup.title.text.split('|')[1]
    else:
        title = soup.title.text

    if is_exit(title,img_url,publish_time):
        print('already exit')
        return
    else:
        item_id += 1
        typeId = get_type_id(type_name)
        print('img_url:'+img_url)

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
        mComposition.set('source_name', '恒星英语')
        mComposition.set('category', 'composition')
        mComposition.set('type', 'text')
        mComposition.save()
        print('save item')


def is_exit(str,img_url,publish_time):
    query = Query('Reading')
    query.equal_to('title', str)
    query.equal_to('category', 'composition')
    querys = query.find()
    # if len(querys) > 0:
    #     data = querys[0]
    #     # imgUrl = data.get('img_url')
    #     # ptime = data.get('publish_time')
    #     # print ('odl-imgUrl:'+imgUrl)
    #     # print ('new-imgUrl:'+img_url)
    #     data.set('img_url',img_url)
    #     data.set('publish_time',publish_time)
    #     data.save()
    #     print('save img_url and publish_time')
    return len(querys) > 0

def get_all_link(url):
    global item_id
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url,headers=headers)
    req.encoding='gbk'
    soup = BeautifulSoup(req.text,"html5lib")
    ulstr = soup.find_all(class_='fz18 YaHei fbold')
    dates = soup.find_all('span', class_='gray-9 mr25')

    for i in range(0,len(ulstr)):
        a = ulstr[i].find('a')
        href = a['href']
        print dates[i].text
        if 'html' in href:
            detail_url = 'http://www.hxen.com/'+a['href']
            # publish_time = dates[i].text.lstrip();
            publish_time = datetime.strptime(dates[i].text.lstrip(), "%Y-%m-%d")
            print('catch url:'+detail_url)
            nowplaying_movies(detail_url,publish_time)
        else:
            pass


def get_type_id(type_name):
    if type_name == u'初中英语作文' or type_name == u'中考英语作文':
        return '1003'
    elif type_name == u'小学英语作文':
        return '1004'
    elif type_name == u'高考英语作文' or type_name == u'高中英语作文' or type_name == u'成人高考英语作文':
        return '1002'
    else:
        return '1001'

def get_lastest_item_id():
    query = Query('Reading')
    query.equal_to('category', 'composition')
    query.equal_to('source_name', '恒星英语')
    query.descending("item_id")
    query.limit(1)
    querys = query.find()
    itemId = querys[0].get("item_id")
    return itemId

def task():
    global item_id
    item_id = get_lastest_item_id();
    print('task start %d' % item_id)
    url = 'http://www.hxen.com/englishwriting/index.html'
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




