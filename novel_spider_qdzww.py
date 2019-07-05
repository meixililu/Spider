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

def parse_detail(url,title,author,des):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, "html5lib")

    img_url = ''
    read_url = ''
    update = ''
    viewstr_n = ''
    tagstr = ''
    views = 0
    read_tag = soup.find('a',class_='red-btn J-getJumpUrl ')
    if read_tag:
        read_url = urlparse.urljoin(url,read_tag['href'])

    img_tag = soup.select('div.book-img > a > img')
    if len(img_tag) > 0:
        img_url = urlparse.urljoin(url,img_tag[0]['src'])

    views_tag = soup.find('span',class_='twtIRjBn')
    print views_tag
    if views_tag:
        viewstr_n = views_tag.text.strip()

    tags_tag = soup.select('p.tag > a')
    if len(tags_tag) > 0:
        for item in tags_tag:
            tagstr += item.text
            tagstr += " "

    # span = soup.select('span.text b')
    # if len(span) > 1:
    #     viewstr = span[2].text.strip()
    #     if u'亿' in viewstr:
    #         viewstr = viewstr.replace(u'亿','')
    #         views = float(viewstr) * 100000000
    #     elif u'万' in viewstr:
    #         viewstr = viewstr.replace(u'万','')
    #         views = float(viewstr) * 10000
    #     elif u',' in viewstr:
    #         viewstr = viewstr.replace(u',', '')
    #         views = float(viewstr)
    #     else:
    #         views = float(viewstr)

    author_tag = soup.find('span',class_='first')
    if author_tag:
        author = author_tag.text

    print title
    print author
    print tagstr
    print des
    print url
    print read_url
    print img_url
    print views
    print viewstr_n

    if len(title) == 0:
        return

    if is_exit(title,url,update,views):
        print 'url is exit'
        return

    Composition = Object.extend('novel')
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
    mComposition.set('source_name', "起点中文网")
    mComposition.set('views', views)
    mComposition.set('viewstr', viewstr_n)
    # mComposition.save()
    print('save item')



def get_list(url):
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url,headers=headers)
    req.encoding='utf-8'
    soup = BeautifulSoup(req.text,"html5lib")
    links = soup.select('ul.all-img-list.cf li')
    print len(links)
    for link in links:
        detail_url = ''
        author = ''
        title = ''
        des = ''
        next_tag = link.select('div.book-img-box a')
        if len(next_tag)>0:
            detail_url = urlparse.urljoin(url,next_tag[0]['href'])
        author_tag = link.select('p.author > a')
        if len(author_tag) > 0:
            author = author_tag[0].text
        title_tag = link.find('h4')
        if title_tag:
            title = title_tag.text
        des_tag = link.find('p',class_='intro')
        if des_tag:
            des = des_tag.text.strip()


        # print detail_url
        # print title
        # print author
        # print des

        parse_detail(detail_url,title,author,des)


def task():
    # 49506
    for i in range(1,506):
        url = 'https://www.qidian.com/free/all?orderId=&vip=hidden&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=1&page=%d'%(i)
        print url
        get_list(url)


if __name__ == '__main__':
    task()