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
import re
import traceback

leancloud.init('3fg5ql3r45i3apx2is4j9on5q5rf6kapxce51t5bc0ffw2y4', 'twhlgs6nvdt7z7sfaw76ujbmaw7l12gb8v6sdyjw1nzk9b1a')

def isExit(title):
    global category
    query = Query('HJWordStudyCList')
    query.equal_to('category', category)
    query.equal_to('title', title)
    querys = query.find()
    return len(querys) > 0

def getType(type_name):
    query = Query('HJWordStudyCategory')
    query.equal_to('name', type_name)
    querys = query.find()
    if len(querys) > 0:
        data = querys[0]
        return data.get('type_code')
    else:
        print 'not exit'

def get_item(url):
    global category
    global type_code
    global isStart
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url,headers=headers)
    req.encoding='utf-8'
    soup = BeautifulSoup(req.text,"html5lib")
    alinks = soup.find_all('a', class_='n nolink')
    for link in alinks:
        type_code = getType(link.text.strip())
        print link.text.strip()
        print category
        print type_code
        item_links = link.find_next_sibling().find_all('a')
        for item in item_links:
            print item.text
            # if item.text == 'meet':
            #     isStart = True
            # if isStart:
            parseDetailPage('http://www.hujiang.com' + item['href'],item.text)

def parseDetailPage(url,word):
    # url = 'http://www.hujiang.com/ciku/noresult/'
    try:
        print url
        global category
        global type_code
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
        req = requests.get(url, headers=headers)
        req.encoding = 'utf-8'
        content = req.text.replace('<br>','\n')
        content = content.replace('<br />','\n')
        content = content.replace('<br/>','\n')
        soup = BeautifulSoup(content, "html5lib")
        article_content = soup.find('div',id="article_content")
        article_title = soup.find('h1',id='article_title')
        if article_title and article_content:
            title = article_title.text.strip()
            content = getContent(article_content.text.strip(),title)
            if isExit(title):
                print 'exit and return'
                return
            else:
                print word
                print title
                print content
                FilmDetail = Object.extend('HJWordStudyCList')
                mFilmDetail = FilmDetail()
                mFilmDetail.set('title', title)
                mFilmDetail.set('word', word)
                mFilmDetail.set('word_des', content)
                mFilmDetail.set('category', category)
                mFilmDetail.set('type', type_code)
                mFilmDetail.set('source_url', url)
                mFilmDetail.save()
                print('save item')
        else:
            print 'has no result'
    except:
        print 'exception:' + word
        print traceback.format_exc()
        FilmDetail = Object.extend('HJWordStudyCList')
        mFilmDetail = FilmDetail()
        mFilmDetail.set('word', word)
        mFilmDetail.set('category', category)
        mFilmDetail.set('type', type_code)
        mFilmDetail.set('source_url', url)
        mFilmDetail.save()


def getContent(content,title):
    print title
    contents = ''
    for conn in content.splitlines():
        con = conn.strip()
        if con is None:
            continue
        elif title in con or u'沪江词库' in con or u'换一组' in con or u'更多翻译' in con or u'更多句子' in con or u'更多短语' in con or u'由沪江网提供' in con or u'显示全部' in con or u'到沪江小D' in con:
            continue
        elif u'更多单词' in con:
            break
        # elif u'金山词霸微信版开通啦' in con or u'点击进入' in con or u'专为' in con or u'您的浏览器' in con or u'求关注' in con or 'ijinshanciba' in con or u'帐号：' in con or u'号外号外' in con:
        #     pass
        elif len(con) == 0:
            continue
        else:
            contents += con.strip()
            contents += '\n\n'

    return contents

category = ''
type_code = ''
isStart = False
def get_urls():
    global category
    urls = []
    urls.append('http://www.hujiang.com/ciku/zuixincy/')
    urls.append('http://www.hujiang.com/ciku/zuixinyingyusijicihui/')
    urls.append('http://www.hujiang.com/ciku/zuixinyingyuliujicihui/')
    urls.append('http://www.hujiang.com/ciku/zuixinkaoyanyingyucihui/')
    urls.append('http://www.hujiang.com/ciku/zuixinkuaijicihui/')
    urls.append('http://www.hujiang.com/ciku/zuixinshangwucihui/')
    urls.append('http://www.hujiang.com/ciku/zuixinzhichengcihui/')
    urls.append('http://www.hujiang.com/ciku/zuixinxiaoxuecihui/')
    urls.append('http://www.hujiang.com/ciku/zuixinchuzhongcihui/')
    urls.append('http://www.hujiang.com/ciku/zuixingaozhongcihui/')
    urls.append('http://www.hujiang.com/ciku/zuixinjisuanjicihui/')
    urls.append('http://www.hujiang.com/ciku/zuixinwaimaocihui/')

    for url in urls:
        if 'zuixincy' in url:
            category = '1001'
        elif 'zuixinyingyusijicihui' in url:
            category = '1002'
        elif 'zuixinyingyuliujicihui' in url:
            category = '1003'
        elif 'zuixinkaoyanyingyucihui' in url:
            category = '1004'
        elif 'zuixinkuaijicihui' in url:
            category = '1005'
        elif 'zuixinshangwucihui' in url:
            category = '1006'
        elif 'zuixinzhichengcihui' in url:
            category = '1007'
        elif 'zuixinxiaoxuecihui' in url:
            category = '1008'
        elif 'zuixinchuzhongcihui' in url:
            category = '1009'
        elif 'zuixingaozhongcihui' in url:
            category = '1010'
        elif 'zuixinjisuanjicihui' in url:
            category = '1011'
        elif 'zuixinwaimaocihui' in url:
            category = '1012'
        print category
        print url
        get_item(url)


if __name__ == '__main__':
    # get_item('http://www.hujiang.com/ciku/zuixinyingyusijicihui/')
    get_urls()