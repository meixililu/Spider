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

def is_exit(name,url,update,views):
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

def parse_detail(url,img_url,title,update):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, "html5lib")

    read_url = ''
    des = ''
    author = ''
    tagstr = ''
    views = 0
    author_tag = soup.find('span',class_='name')
    if author_tag:
        author = author_tag.text.strip()

    tags_tag = soup.select('span.text > b')
    if len(tags_tag) > 0:
        tagstr = tags_tag[0].text.strip()

    des_tag = soup.find('p',class_='intro-total')
    if des_tag:
        des = des_tag.text.strip()

    read_tag = soup.find('a',class_='btn--read')
    if read_tag:
        read_url = 'https://m.mkzhan.com'+read_tag['href']

    span = soup.select('span.text b')
    if len(span) > 1:
        viewstr = span[2].text.strip()
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

    author_tag = soup.find('span',class_='first')
    if author_tag:
        author = author_tag.text

    print title
    print tagstr
    print author
    print des
    print read_url
    print img_url
    print views

    if len(title) == 0:
        return

    if is_exit(title,url,update,views):
        print 'url is exit'
        return

    Composition = Object.extend('Caricature')
    mComposition = Composition()
    mComposition.set('name', title)
    mComposition.set('author', author)
    mComposition.set('book_img_url', img_url)
    mComposition.set('category', "")
    mComposition.set('des', des)
    mComposition.set('read_url', read_url)
    mComposition.set('tag', tagstr)
    mComposition.set('type', "")
    mComposition.set('update', update)
    mComposition.set('url', url)
    mComposition.set('source_name', "漫客栈")
    mComposition.set('views', views)
    mComposition.save()
    print('save item')



def get_list(url):
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url,headers=headers)
    req.encoding='utf-8'
    soup = BeautifulSoup(req.text,"html5lib")
    links = soup.find_all('div',class_='common-comic-item')
    print len(links)
    for link in links:
        img_tag = link.find('img')
        img = ''
        title = ''
        update = ''
        if img_tag:
            img = img_tag['data-src']
        a_tag = link.find('a',class_='cover')
        if a_tag:
            detail_url = urlparse.urljoin(url,a_tag['href'])
        p_tag = link.find('p',class_='comic__title')
        if p_tag:
            title = p_tag.text.strip()

        update_tag = link.find('p',class_='comic-update')
        if update_tag:
            update = update_tag.text.strip()

        parse_detail(detail_url,img,title,update)


def task():
    for i in range(1,126):
        url = 'https://www.mkzhan.com/category/?page=%d'%(i)
        print url
        get_list(url)


if __name__ == '__main__':
    task()