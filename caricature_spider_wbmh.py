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

def parse_detail(url,title,cover):
    global viewstime
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
        browser = webdriver.PhantomJS(executable_path='/Users/luli/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs')
        browser.get(url)

        time.sleep(1)
        tagstr = ''
        read_url = ''
        author = ''
        des = ''
        views_str = ''
        update = ''
        viewstime = viewstime - 120
        views = viewstime

        soup = BeautifulSoup(browser.page_source, "html5lib")

        author_tag = soup.select('div.comicStatus.clearfix > p')
        if len(author_tag) > 0:
            author = author_tag[0].text.encode('utf-8').strip()

        tagstr_tag = soup.select('div.comicStatus.clearfix > p > span')
        if len(tagstr_tag) > 1:
            tagstr = tagstr_tag[1].text.encode('utf-8').strip().replace('、',' ')

        des_tag = soup.find('div',class_='comicDesc')
        if des_tag:
            des = des_tag.text.strip()

        read_btn = browser.find_element_by_class_name('readNow')
        read_btn.click()
        time.sleep(0.5)
        read_url = browser.current_url

        print title
        print tagstr
        print author
        print des
        print read_url
        print url
        print views_str
        print views
        print update

        if len(read_url) > 0 and read_url != url:

            if is_exit(title,url,update,views):
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
            mComposition.set('source_name', "微博动漫")
            mComposition.set('views', views)
            mComposition.save()
            print('save item')
    except:
        print 'exception skip'
        print traceback.format_exc()

def get_list(url):
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url,headers=headers)
    result = json.loads(req.text)
    for book in result['data']['data']:
        title = book['comic_name']
        cover = book['comic_cover']
        book_url = 'http://manhua.weibo.com/c/' + book['comic_id']
        # print title
        # print cover
        # print book_url
        parse_detail(book_url,title,cover)

viewstime = 489280
def task():
    for i in range(120,121):
        print 'page:'+str(i)
        url = 'http://manhua.weibo.cn/wbcomic/comic/filter_result?rows_num=16&cate_id=0&end_status=0&comic_pay_status=0&order=comic_read_num&_debug_=yes&_request_from=pc&page_num=%d'%(i)
        print url
        get_list(url)

if __name__ == '__main__':
    task()