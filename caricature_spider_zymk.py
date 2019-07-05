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

def parse_detail(url,title):
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
    mComposition.set('source_name', "知音漫客")
    mComposition.set('views', views)
    mComposition.save()
    print('save item')



def get_list(page):
    url = "https://api.zymk.cn/app_api/v5/getsortlist_new/?callback=getsortlistNewCb&type=all&sort=click&key=&client-type=wap&_=1537172639672&page="+str(page)
    headers = {'User-Agent' : 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Mobile Safari/537.36'}

    req = requests.get(url,headers=headers)
    result = req.text.replace('getsortlistNewCb(','')
    result = result.replace(');','')
    result = json.loads(result)
    for book in result['data']['page']['comic_list']:
        title = book['comic_name']
        book_url = 'https://m.zymk.cn/'+ str(book['comic_id'])
        parse_detail(book_url,title)

def task():
    for i in range(1,67):
        print 'page:'+str(i)
        get_list(i)


if __name__ == '__main__':
    task()