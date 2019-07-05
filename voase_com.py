# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import leancloud
from leancloud import Object
from leancloud import Query
from datetime import *
import time
import traceback
import urlparse
import contentUtil


leancloud.init('3fg5ql3r45i3apx2is4j9on5q5rf6kapxce51t5bc0ffw2y4', 'twhlgs6nvdt7z7sfaw76ujbmaw7l12gb8v6sdyjw1nzk9b1a')

def is_exit(str,url):
    global category
    query = Query('Reading')
    query.equal_to('title', str)
    query.equal_to('category', category)
    query.equal_to('source_url', url)
    querys = query.find()
    return len(querys) > 0

def parse_detail(url,publish_time):
    global source_name
    global category
    global type
    global item_id
    global category_2
    global type_name
    # url = 'http://www.51voa.com/VOA_Videos/february-14-2019-81431.html'
    title = ''
    contents = ''
    img_url = ''
    media_url = ''
    lrc_url = ''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, "html5lib")
    try:

        source_tag = soup.find('source')
        if source_tag:
            media_url = source_tag['src']
            img_video_tag = soup.find('video',id='51VOA_Video')
            type = 'video'
            if img_video_tag:
                img_url = urlparse.urljoin(url, img_video_tag['poster'])

        EnPage_tag = soup.find('a', id='EnPage')
        if EnPage_tag:
            detailUrl = urlparse.urljoin(url, EnPage_tag['href'])
            parse_detail(detailUrl)
            return

        div_tag = soup.find('div',id='title')
        if div_tag:
            title = div_tag.text.strip()

        mp3_tag = soup.find('a',id='mp3')
        if mp3_tag:
            media_url = mp3_tag['href']
            type = 'mp3'

        lrc_tag = soup.find('a',id='lrc')
        if lrc_tag:
            lrc_url = urlparse.urljoin(url, lrc_tag['href'])

        img_tag = soup.select('div#content img')
        if len(img_tag) > 0:
            img_url = img_tag[0]['src']

        content_tag = soup.select('div#content')
        if len(content_tag) > 0:
            contents = contentUtil.get51voaContent(content_tag[0].text.strip())


        if is_exit(title,url):
            pass
            # print 'item exit'
        else:
            # print title
            # print img_url
            # print lrc_url
            # print media_url
            # print publish_time
            # print source_name
            # print category
            # print type
            # print category_2
            # print type_name
            # print contents
            if len(media_url.strip()) == 0:
                return
            Composition = Object.extend('Reading')
            mComposition = Composition()
            mComposition.set('title', title)
            mComposition.set('img_url', img_url)
            mComposition.set('img_type', 'url')
            mComposition.set('content', contents)
            mComposition.set('type_name', type_name)
            mComposition.set('publish_time', publish_time)
            mComposition.set('type_id', '')
            mComposition.set('source_url', url)
            mComposition.set('source_name', source_name)
            mComposition.set('category', category)
            mComposition.set('category_2', category_2)
            mComposition.set('lrc_url', lrc_url)
            mComposition.set('type', type)
            mComposition.set('media_url', media_url)
            mComposition.save()
            # print 'save item'

    except:
        # print traceback.format_exc()
        # print url
        return

def parse_VOA_Special_English(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, "html5lib")
    try:
        alinks = soup.select('div#list li')
        # print len(alinks)
        for link in alinks:
            alinks = link.find_all('a')
            if len(alinks) > 1:
                nextUrl = urlparse.urljoin(url, alinks[1]['href'])
            # print 'parse_title_list:' + nextUrl
            tempText = link.text
            tempText = tempText[tempText.index('(') + 1:tempText.index(')')]
            parse_detail(nextUrl, datetime.strptime(tempText, "%Y-%m-%d"))

    except:
        # print traceback.format_exc()
        # print url
        return

def parse_VOA_Videos(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, "html5lib")
    try:
        alinks = soup.select('div#list li')
        # print len(alinks)
        for link in alinks:
            alink = link.find('a')
            nextUrl = urlparse.urljoin(url, alink['href'])
            # print 'parse_title_list:' + nextUrl
            tempText = link.text
            tempText = tempText[tempText.index('(') + 1:tempText.index(')')]
            parse_detail(nextUrl, datetime.strptime(tempText, "%y-%m-%d"))

    except:
        # print traceback.format_exc()
        # print url
        return


item_id = 0
source_name = u'VOA慢速英语精听网'
category = u'listening'
type_name = u'51voa'
category_2 = 'voa'
type = 'text'

def voa51():
    urls = ["http://www.51voa.com/VOA_Special_English/",
            "http://www.51voa.com/VOA_English_Learning/",
            "http://www.51voa.com/Learning_English_Videos_1.html",
            "http://www.51voa.com/English_in_a_Minute_Videos_1.html",
            "http://www.51voa.com/English_at_the_Movies_1.html",
            "http://www.51voa.com/Everyday_Grammar_TV_1.html",
            "http://www.51voa.com/News_Words_1.html"
            ]
    parse_VOA_Special_English(urls[0])
    parse_VOA_Special_English(urls[1])
    parse_VOA_Videos(urls[2])
    parse_VOA_Videos(urls[3])
    parse_VOA_Videos(urls[4])
    parse_VOA_Videos(urls[5])
    parse_VOA_Videos(urls[6])


if __name__ == '__main__':
    voa51()