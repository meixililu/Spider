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

def parse_detail(url,tagstr,update):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, "html5lib")

    title = ''
    img_url = ''
    read_url = ''
    des = ''
    author = ''
    views = 0
    title_tag = soup.find('h2',class_='works-intro-title ui-left')
    if title_tag:
        title = title_tag.text

    img_tag = soup.select('div.works-cover.ui-left > a > img')
    if len(img_tag) > 0:
        img_url = img_tag[0]['src']

    des_tag = soup.find('p',class_='works-intro-short ui-text-gray9')
    if des_tag:
        des = des_tag.text.strip()

    read_tag = soup.find('a',class_='works-intro-view ui-btn-orange ui-radius3')
    if read_tag:
        read_url = "http://ac.qq.com"+read_tag['href']

    span = soup.select('p.works-intro-digi span em')
    if len(span) > 1:
        viewstr = span[1].text.strip()
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
    mComposition.set('source_name', "腾讯动漫")
    mComposition.set('views', views)
    mComposition.save()
    print('save item')



def get_list(url):
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url,headers=headers)
    req.encoding='utf-8'
    soup = BeautifulSoup(req.text,"html5lib")
    links = soup.find_all('a',class_='mod-cover-list-thumb mod-cover-effect ui-db')
    tags = soup.find_all('p',class_='ret-works-tags')
    update_tags = soup.find_all('span',class_='mod-cover-list-text')
    print len(links)
    print len(tags)
    print len(update_tags)
    for (index,link) in enumerate(links):
        update = update_tags[index].text
        tag_a = tags[index].find_all('a')
        tagstr = ''
        for a in tag_a:
            tagstr += a.text + ' '
        detail_url = 'http://ac.qq.com' + link['href']
        print detail_url
        print update
        parse_detail(detail_url,tagstr.strip(),update)


def task():
    for i in range(1,2374):
    # for i in range(1,170):
        #all
        url = 'http://ac.qq.com/Comic/all/search/time/page/%d'%(i)
        #pink 精品
        # url = 'http://ac.qq.com/Comic/index/state/pink/page/%d'%(i)
        #free
        # url = 'http://ac.qq.com/Comic/all/search/time/vip/1/page/%d'%(i)
        # #vip
        # url = 'http://ac.qq.com/Comic/all/search/time/vip/2/page/%d' % (i)
        print url
        get_list(url)


if __name__ == '__main__':
    task()