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
from selenium import webdriver
import traceback

leancloud.init('3fg5ql3r45i3apx2is4j9on5q5rf6kapxce51t5bc0ffw2y4', 'twhlgs6nvdt7z7sfaw76ujbmaw7l12gb8v6sdyjw1nzk9b1a')

def is_exit(name,url):
    query = Query('Caricature')
    query.equal_to('name', name)
    query.equal_to('url', url)
    querys = query.find()

    return len(querys) > 0

def parse_detail(url,title,update,author,views):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
        browser = webdriver.PhantomJS(executable_path='/Users/luli/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs')
        browser.get(url)

        time.sleep(1)
        tagstr = ''
        read_url = ''
        cover = ''
        views_str = ''
        des = ''

        soup = BeautifulSoup(browser.page_source, "html5lib")

        read_url_tag = soup.find('a',class_='btn btn-arr btn-blue')
        if read_url_tag:
            read_url = read_url_tag['href']

        img_tag = soup.select('div.fl.detail-cover-img > img')
        if len(img_tag) > 0:
            cover = img_tag[0]['data-src']

        tagstr_tag = soup.select('span.fr.detail-span-cate > a')
        if len(tagstr_tag) > 0:
            for item in tagstr_tag:
                tagstr += item.text.strip()
                tagstr += " "

        des_tag = soup.find('p',class_='detail-cover-desc')
        if des_tag:
            des = des_tag.text.strip()

        if views > 100000000:
            temp = views/100000000
            views_str = str(round(temp, 1)) + '亿'
        elif views > 10000:
            temp = views/10000
            views_str = str(round(temp, 1)) + '万'
        else:
            views_str = str(views)



        print title
        print tagstr
        print author
        print cover
        print des
        print read_url
        print url
        print views_str
        print views
        print update

        if len(read_url) > 0 and read_url != url:

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
            mComposition.set('tag', tagstr)
            mComposition.set('isFree', '')
            mComposition.set('viewstr', views_str)
            mComposition.set('type', "")
            mComposition.set('update', update)
            mComposition.set('url', url)
            mComposition.set('source_name', "可米酷")
            mComposition.set('views', views)
            mComposition.save()
            print('save item')
    except:
        print 'exception skip'
        print traceback.format_exc()

def get_list(url):
    global comic_id
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url,headers=headers)
    result = req.text.replace('jsonp_allcomic(', '')
    result = result.replace(')', '')
    result = json.loads(result)
    if result['content_list']:
        for book in result['content_list']:
            title = book['content_title']
            update = book['content_desc_lite']
            author = book['content_subtitle']
            comic_id = book['content_action']
            views = book['content_praise_count']
            book_url = 'https://comicool.cn/content/detail.html?comic_id=' + book['content_action']
            parse_detail(book_url, title, update, author, views)
        task()


viewstime = 100000
comic_id = '0'
def task():
    global comic_id
    url = 'https://proxy.comicool.cn/allcomic4h5?callback=jsonp_allcomic&page_size=48&page_direction=2&list_type=category&order_type=rating&req_id=62&req_param=1&comic_id='+(comic_id)
    print url
    get_list(url)

if __name__ == '__main__':
    task()