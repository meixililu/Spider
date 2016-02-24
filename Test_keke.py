import requests
from bs4 import BeautifulSoup
import json
import leancloud
from leancloud import Object
from leancloud import Query

leancloud.init('3fg5ql3r45i3apx2is4j9on5q5rf6kapxce51t5bc0ffw2y4', 'twhlgs6nvdt7z7sfaw76ujbmaw7l12gb8v6sdyjw1nzk9b1a')

def nowplaying_movies(url):
    global item_id
    contents = ''
    img_url = ''
    type_name = ''
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url,headers=headers)
    req.encoding='gbk'
    soup = BeautifulSoup(req.text,"html5lib")

    div = soup.find('div',id='arctext')
    if div == None:
        print(div)
        print('div == none:')
        return

    size = len(div.find_all('p'))
    if size > 0:
        image = soup.p.img
        start = 0
        if image != None:
            img_url = image.attrs["src"]
            start = 1

        for i in range(start,size):
            contents += div.find_all('p')[i].text
            contents += '\n'
    else:
        print('return')
        return

    if contents.strip() == '':
        print('contents == kong')
        return

    titles = soup.title.text.split('|')
    title_size = len(titles)
    if title_size > 1:
        title = soup.title.text.split('|')[0]
        type_name = soup.title.text.split('|')[1]
    else:
        title = soup.title.text

    if is_exit(title):
        print('already exit')
        return
    else:
        item_id += 1
        Composition = Object.extend('Composition')
        mComposition = Composition()
        mComposition.set('item_id', item_id)
        mComposition.set('title', title)
        mComposition.set('img_url', img_url)
        mComposition.set('img_type', 'url')
        mComposition.set('content', contents)
        mComposition.set('type_name', type_name)
        mComposition.set('type_id', '1001')
        mComposition.set('source_url', url)
        mComposition.save()
        print('save item')


def is_exit(str):
    query = Query('Composition')
    query.equal_to('title', str)
    querys = query.find()
    return len(querys) > 0

def get_all_link(url):

    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    req = requests.get(url,headers=headers)
    req.encoding='gbk'
    soup = BeautifulSoup(req.text,"html5lib")
    ulstr = soup.find(class_='imgTxtBar clearfix imgTxtBar-b').find_all('a')

    for a in ulstr:
        href = a['href']
        # print(href)
        if 'html' in href:
            detail_url = 'http://www.hxen.com/'+a['href']
            print('catch url:'+detail_url)
            nowplaying_movies(detail_url)
        else:
            pass


item_id = 1005145
if __name__ == '__main__':
    # for i in range(2,0,-1):
        # gaozhongyingyuzuowen
        # chuzhongyingyuzuowen/
        # xiaoxueyingyuzuowen
        # kaoyanyingyuzuowen
        # liuxuewenshuxiezuo
        # yingyuriji
        # chengrengaokao  
        # CET6
        # yyscb
        # zhuansi
        # zhuanba
        # zhongkaoyingyuzuowen
        # daxueyingyuzuowen
        # qingshu
        # if i == 1:
            url = 'http://www.hxen.com/englishwriting/chengrengaokao/'
        # else:
        #     url = 'http://www.hxen.com/englishwriting/zhuanba/index_%d.html'% i
            print('root url:'+url)
            get_all_link(url)






