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

def parse_detail(url,title,cover,des,author):
    headers = {'User-Agent': "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Mobile Safari/537.36"}
    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, "html5lib")

    views = 0
    viewstr = ''
    read_url = ''
    author = ''
    cover = ''
    tags = ''
    des = ''
    author_tag = soup.find('span',class_='author')
    if author_tag:
        author = author_tag.text.strip()
    des_tag = soup.find('p',class_='content')
    if des_tag:
        des = des_tag.text.strip()
    views_tag = soup.find('span',class_='hasread ift-fire')
    if views_tag:
        viewstr = views_tag.text.strip()
    tags_tag = soup.select('span.tags-txt')
    if len(tags_tag) > 0:
        for item in tags_tag:
            tags += item.text.strip()
            tags += ' '
    a_tag = soup.find('a',class_='read')
    if a_tag:
        read_url = urlparse.urljoin(url, a_tag['href'])
    img_tag = soup.select('div.thumbnail > img')
    if img_tag:
        cover = img_tag[0]['data-src']

    viewstr_n = viewstr
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
    print cover
    print tags
    print url
    print views
    print viewstr_n
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
    mComposition.set('tag', tags)
    mComposition.set('isFree', '')
    mComposition.set('type', "")
    mComposition.set('viewstr', viewstr_n)
    mComposition.set('update', "")
    mComposition.set('url', url)
    mComposition.set('source_name', "漫客岛")
    mComposition.set('views', views)
    # mComposition.save()
    print('save item')



def get_list(page):
    url = "http://www.manhuadao.cn/Comic/Search?t=1537176823151&pageSize=10&comicChannel=&isFinish=&comicNature=&time=&hot=0&comicType=&page="+str(page)
    headers = {'User-Agent' : 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Mobile Safari/537.36'}
    print url
    req = requests.get(url,headers=headers)
    result = json.loads(req.text)
    # print result['html']
    title = ''
    cover = ''
    des = ''
    author = ''
    detail_url = ''
    soup = BeautifulSoup(result['html'], "html5lib")
    lists = soup.find_all('div',class_='item clearfix')
    for item in lists:
        title_tag = item.find('h2')
        if title_tag:
            title = title_tag.text.strip()
        img_tag = item.find('img')
        if img_tag:
            cover = img_tag['src']
        des_tag = item.select('div.brief p')
        if len(des_tag) > 0:
            des = des_tag[0].text.strip()
        author_tag = item.select('div.item-right > p > span > a')
        if len(author_tag) > 0:
            author = author_tag[0].text.strip()
        a_tag = item.select('div.item-right > a')
        if len(a_tag) > 0:
            detail_url = urlparse.urljoin(url,a_tag[0]['href'])
        # print title
        # print cover
        # print des
        # print author
        # print detail_url
        parse_detail(detail_url,title,cover,des,author)

def task():
    for i in range(1,786):
        print 'page:'+str(i)
        get_list(i)


if __name__ == '__main__':
    task()