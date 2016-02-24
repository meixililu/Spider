# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import leancloud
from leancloud import Object
from leancloud import Query
import time
import re

leancloud.init('3fg5ql3r45i3apx2is4j9on5q5rf6kapxce51t5bc0ffw2y4', 'twhlgs6nvdt7z7sfaw76ujbmaw7l12gb8v6sdyjw1nzk9b1a')

def nowplaying_movies(url):
    global item_id
    contents = ''
    img_url = ''
    type_name = ''
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url,headers=headers)
    # req.encoding='utf-8'
    soup = BeautifulSoup(req.text,"html5lib")
    [script.extract() for script in soup.findAll('script')]
    [style.extract() for style in soup.findAll('style')]

    title = soup.find('div',class_='list_left_list').find('h1').text

    if is_exit(title):
        print('already exit')
        return

    your_string = soup.find('div',class_='contentmain').get_text()
    p=re.compile('\s+ ')
    contents = re.sub(p,'',your_string)
    contents = contents.replace('\n\n\n', '\n')

    type_name = soup.find('li',id='select').find('a').text
    # p = soup.find('div',class_='contentmain').find_all('p')
    # if len(p) > 0:
    #     for i in range(0,len(p)):
    #         contents += p[i].text
    #         contents += '\n'
    # else:
    #     contents = soup.find('div',class_='content-ad').next_sibling
    #     contents += '\n'
    #     contents += soup.find('div',class_='content-ad').next_sibling.next_sibling.next_sibling

    typeId = get_type_id(type_name)

    print(title)
    print(type_name)
    print(typeId)
    print(item_id)
    print(contents)

    item_id += 1
    Composition = Object.extend('Composition')
    mComposition = Composition()
    mComposition.set('item_id', item_id)
    mComposition.set('title', title)
    mComposition.set('img_url', img_url)
    mComposition.set('img_type', 'url')
    mComposition.set('content', contents)
    mComposition.set('type_name', type_name)
    mComposition.set('type_id', typeId)
    mComposition.set('source_url', url)
    mComposition.set('source_name', '水滴英语作文网')
    mComposition.save()
    print('save item')


def is_exit(str):
    query = Query('Composition')
    query.equal_to('title', str)
    querys = query.find()
    return len(querys) > 0

def get_all_link(url):
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url,headers=headers)
    req.encoding='utf-8'
    soup = BeautifulSoup(req.text,"html5lib")

    ulstr = soup.find(class_='content-list').find_all('li')

    for li in ulstr:
        a = li.find('a')
        href = a['href']
        detail_url = 'http://www.adreep.cn'+a['href']
        print('catch url:'+detail_url)
        nowplaying_movies(detail_url)

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
    query = Query('Composition')
    query.descending("item_id")
    query.equal_to('source_name', '水滴英语作文网')
    query.limit(1)
    querys = query.find()
    if len(querys) == 0:
        return 0
    else:
        return querys[0].get("item_id")

item_id = 0
def task():
    item_id = get_lastest_item_id();
    print('task start %d' % item_id)
    list = {'xx','cz','gz','dxyy','fw'}
    for li in list:
        for i in range(1,0,-1):
            url = "http://www.adreep.cn/%s/?page=%d" %(li,i)
            print(url)
            get_all_link(url)



if __name__ == '__main__':
    # url = "http://www.adreep.cn/xx/54939.html"
    # nowplaying_movies(url)
    task()




