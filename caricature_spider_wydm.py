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

def is_exit(name,url,update,views):
    query = Query('Caricature')
    query.equal_to('name', name)
    query.equal_to('url', url)
    querys = query.find()
    if len(querys) > 0:
        data = querys[0]
        data.set('update', update)
        data.set('views', views)
        data.save()
        print 'update success'

    return len(querys) > 0

def parse_detail(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, "html5lib")

    a_tags = soup.select('dl.sr-dl > dd > a')
    print len(a_tags)
    tags = ''
    if len(a_tags) > 0:
        for a in a_tags:
            if len(a.attrs) > 2:
                tags += a.attrs['title'] + ' '

    return tags.strip()








def get_list(url):
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url,headers=headers)
    result = json.loads(req.text)
    for book in result['books']:
        title = book['title']
        book_url = 'https://manhua.163.com/source/' + book['bookId']
        read_url = 'https://manhua.163.com/reader/' + book['bookId']
        des = ''
        if book.has_key('announcement'):
            des = book['description'] + ' ' + book['announcement']
        else:
            des = book['description']
        author = book['author']
        views = float(book['clickCount'])
        update = book['latestSectionTitle']
        book_img_url = book['cover']
        isFree = '0'
        if book['payTypeEnum'] == 'BY_ARTICLE':
            isFree = '1'
        else:
            isFree = '0'


        print title
        print author
        print des
        print read_url
        print book_img_url
        print views

        if is_exit(title,book_url,update,views):
            print 'url is exit'
            return

        tagstr = parse_detail(book_url)
        print tagstr

        Composition = Object.extend('Caricature')
        mComposition = Composition()
        mComposition.set('name', title)
        mComposition.set('author', author)
        mComposition.set('book_img_url', book_img_url)
        mComposition.set('category', "")
        mComposition.set('des', des)
        mComposition.set('read_url', read_url)
        mComposition.set('tag', tagstr)
        mComposition.set('isFree', isFree)
        mComposition.set('type', "")
        mComposition.set('update', update)
        mComposition.set('url', book_url)
        mComposition.set('source_name', "网易动漫")
        mComposition.set('views', views)
        mComposition.save()
        print('save item')

def task():
    # 66
    for i in range(1,66):
        url = 'https://manhua.163.com/category/getData.json?sort=2&pageSize=72&page=%d'%(i)
        print url
        get_list(url)


if __name__ == '__main__':
    task()