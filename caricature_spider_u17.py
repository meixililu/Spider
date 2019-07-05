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
import urlparse
leancloud.init('3fg5ql3r45i3apx2is4j9on5q5rf6kapxce51t5bc0ffw2y4', 'twhlgs6nvdt7z7sfaw76ujbmaw7l12gb8v6sdyjw1nzk9b1a')

def is_exit(name,url):
    query = Query('Caricature')
    query.equal_to('name', name)
    query.equal_to('url', url)
    querys = query.find()
    # if len(querys) > 0:
    #     data = querys[0]
    #     data.set('update', update)
    #     data.set('views', views)
    #     data.save()
    #     print 'update success'

    return len(querys) > 0

def parse_detail(url,title,tag,cover,update):
    headers = {'User-Agent': "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Mobile Safari/537.36"}
    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, "html5lib")

    views = 0
    viewstr = ''
    read_url = ''
    author = ''
    des = ''
    author_tag = soup.find('div',class_='author-name')
    if author_tag:
        author = author_tag.text
    intro = soup.find('div',class_='comic-intro')
    if intro:
        des = intro.text.strip()
    renqi = soup.select('div.comic-renqi span')
    if renqi:
        views_str = renqi[0].text.strip()
        viewstr = renqi[0].text.strip()
        print viewstr
        if u'亿' in viewstr:
            viewstr = viewstr.replace(u'亿','')
            views = float(viewstr) * 100000000
        elif u'万' in viewstr:
            viewstr = viewstr.replace(u'万','')
            views = float(viewstr) * 10000
        elif u',' in viewstr:
            viewstr = viewstr.replace(u',', '')
            views = float(viewstr)
        else:
            views = float(viewstr)
    read = soup.select('div.comic-btn-box a')
    if read:
        read_url = urlparse.urljoin(url, read[0]['href'])

    print title
    print author
    print read_url
    print url
    print views
    print views_str
    print des
    if is_exit(title,url):
        print 'url is exit'
        return

    Composition = Object.extend('Caricature')
    mComposition = Composition()
    mComposition.set('name', title)
    mComposition.set('author', author)
    mComposition.set('book_img_url', cover)
    mComposition.set('category', "")
    mComposition.set('des', des)
    mComposition.set('read_url', read_url)
    mComposition.set('tag', tag)
    mComposition.set('isFree', '')
    mComposition.set('type', "")
    mComposition.set('viewstr', views_str)
    mComposition.set('update', update)
    mComposition.set('url', url)
    mComposition.set('source_name', "有妖气")
    mComposition.set('views', views)
    mComposition.save()
    print('save item')



def get_list(page):
    url = "http://www.u17.com/comic/ajax.php?mod=comic_list&act=comic_list_new_fun&a=get_comic_list"
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    postData = {
        "data[group_id]":"no",
        "data[theme_id]":"no",
        "data[is_vip]":"no",
        "data[accredit]":"no",
        "data[color]":"no",
        "data[comic_type]":"no",
        "data[series_status]":"no",
        "data[order]": 0,
        "data[page_num]":page,
        "data[read_mode]":"no"
    }
    req = requests.post(url,headers=headers,data=postData)
    result = json.loads(req.text)
    # print req.text
    for book in result['comic_list']:
        title = book['name']
        book_url = 'http://m.u17.com/c/'+ book['comic_id'] +'.html'
        tag = book['line2'].replace('/',' ')
        cover = book['cover']

        print title
        print book_url
        print tag
        print cover
        parse_detail(book_url,title,tag,cover,'')

def task():
    for i in range(68,410):
        print 'page:'+str(i)
        get_list(i)


if __name__ == '__main__':
    task()