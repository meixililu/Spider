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

def parse_detail(url,title,des,cover,likes,author):
    headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}
    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, "html5lib")

    # print req.text
    views = 0
    viewstr = ''
    read_url = ''
    a_tag = soup.select('div.btn.btn-primary a')
    if len(a_tag) > 0:
        read_url = urlparse.urljoin(url, a_tag[0]['href'])


    viewstr = likes
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

    print title
    print author
    print read_url
    print url
    print views
    print likes
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
    mComposition.set('tag', "")
    mComposition.set('isFree', '')
    mComposition.set('type', "")
    mComposition.set('viewstr', likes)
    mComposition.set('update', "")
    mComposition.set('url', url)
    mComposition.set('source_name', "快看漫画")
    mComposition.set('views', views)
    mComposition.save()
    print('save item')



def get_list(page):
    url = "http://www.kuaikanmanhua.com/web/tags/0?count=20&page="+str(page)
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}

    req = requests.get(url,headers=headers)
    result = json.loads(req.text)
    for book in result['data']['topics']:
        title = book['title']
        description = book['description']
        book_url = 'http://www.kuaikanmanhua.com/web/topic/'+ str(book['id'])
        cover = book['vertical_image_url']
        likes = book['likes']
        author = book['user']['nickname']
        parse_detail(book_url,title,description,cover,likes,author)

def task():
    for i in range(0,100):
        print 'page:'+str(i)
        get_list(i)


if __name__ == '__main__':
    task()