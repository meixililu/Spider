# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import leancloud
from leancloud import Object
from leancloud import Query

leancloud.init('3fg5ql3r45i3apx2is4j9on5q5rf6kapxce51t5bc0ffw2y4', 'twhlgs6nvdt7z7sfaw76ujbmaw7l12gb8v6sdyjw1nzk9b1a')


def is_exit(count):
    # Composition
    query = Query('Composition')
    query.ascending('createdAt')
    # print query.count()
    query.skip(count)
    querys = query.find()
    print len(querys)
    size = len(querys)
    if size == 0:
        return

    for data in querys:
        title = data.get('title')
        print(title)

        if is_reading_exit(title):
            print('already exit')
            pass
        else:
            Composition = Object.extend('Reading')
            mComposition = Composition()
            mComposition.set('title', data.get('title'))
            mComposition.set('type_id', data.get('type_id'))
            mComposition.set('content', data.get('content'))
            mComposition.set('source_url', data.get('source_url'))
            mComposition.set('source_name', data.get('source_name'))
            mComposition.set('type_name', data.get('type_name'))
            mComposition.set('publish_time', data.get('publish_time'))
            mComposition.set('item_id', data.get('item_id'))
            mComposition.set('img_type', data.get('img_type'))
            mComposition.set('img_url', data.get('img_url'))
            mComposition.set('type', data.get('type'))
            mComposition.set('category', data.get('category'))
            mComposition.save()

def is_reading_exit(str):
    query = Query('Reading')
    query.equal_to('title', str)
    querys = query.find()
    return len(querys) > 0

if __name__ == '__main__':
    for i in range(63,97):
        print i
        is_exit(i*100)
        # is_exit(0)






