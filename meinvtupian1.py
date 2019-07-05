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
import cStringIO, urllib2
from PIL import Image
import traceback

leancloud.init('3fg5ql3r45i3apx2is4j9on5q5rf6kapxce51t5bc0ffw2y4', 'twhlgs6nvdt7z7sfaw76ujbmaw7l12gb8v6sdyjw1nzk9b1a')


def is_exit(str):
    global category
    query = Query('Joke')
    query.equal_to('text', str)
    querys = query.find()
    return len(querys) > 0

def is_exit_img(img):
    query = Query('Joke')
    query.equal_to('img', img)
    querys = query.find()
    return len(querys) > 0

def getImageRatio(url):
    try:
        send_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive'
        }
        print 'getImageRatio img:' + url
        # url = 'http://wimg.spriteapp.cn/ugc/2017/03/15/58c8b5067cd1adad.gif'
        if len(url) > 5:
            req = urllib2.Request(url, headers=send_headers)
            file = urllib2.urlopen(req)
            tmpIm = cStringIO.StringIO(file.read())
            im = Image.open(tmpIm)
            (width, height) = im.size
            ratio = float(width) / height
            print ratio
            if ratio < 0.04:
                return 0.8
            return ratio
        else:
            print 'error url:' + url
    except urllib2.HTTPError, e:
        print e.code
        if e.code == 404:
            return 5.5555
        if e.code == 403:
            return 5.5555
        print 'except getImageRatio'
        print traceback.format_exc()
        return 5.5555;

sign = '?showapi_appid=11619&showapi_sign=f27574671ec14eb4a97faacb2eee3ef2'
def huabanfuli():
    global sign
    # types=['4001','4002','4003','4004','4007','4010','4011','4012','4013','4014']
    types=['4013','4014']
    for type in types:
        para = '&page=1&num=20&type=%s' % (type)
        url = 'http://route.showapi.com/852-2'+ sign + para
        print url
        req = requests.get(url)
        print req.text
        result = json.loads(req.text)
        if 0 == result['showapi_res_code']:
            allPages = result['showapi_res_body']['pagebean']['allPages']
            print allPages
            if type == '4013':
                allPages = 128
            for page in range(allPages,0,-1):
                para1 = '&page=%s&num=20&type=%s' % (page,type)
                url = 'http://route.showapi.com/852-2' + sign + para1
                print url
                print page
                req = requests.get(url)
                print req.text
                sbody = json.loads(req.text)
                if 0 == sbody['showapi_res_code']:
                    contentlist = sbody['showapi_res_body']['pagebean']['contentlist']
                    if len(contentlist) == 0:
                        print 'contentlist = 0'
                        continue
                    for item in contentlist:
                        title_h = item['title']
                        img_list = item['list']
                        for index, list_item in enumerate(img_list):
                            big_img = list_item['big']
                            title = title_h + str(index+1)

                            if is_exit(title):
                                print 'title exit:' + title
                                continue
                            else:
                                if is_exit_img(big_img):
                                    print 'big_img exit:' + big_img
                                    continue
                                else:
                                    ratio = getImageRatio(big_img)
                                    if ratio == 5.5555:
                                        print '5.5555 exit'
                                        continue
                                    else:
                                        Reading = Object.extend('Joke')
                                        mReading = Reading()
                                        mReading.set('text', title)
                                        mReading.set('img', big_img)
                                        mReading.set('ratio', ratio)
                                        mReading.set('type', '1')
                                        mReading.set('category', '103')
                                        mReading.save()
                                        print('save item')



#category 101 搞笑; 102 段子; 103 美女; 104
#type 1 img; 2 imgs; 3 git; 4 video; 5 text; 6 url；
if __name__ == '__main__':
    huabanfuli();
