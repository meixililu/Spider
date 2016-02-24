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
    query.contains('type_name', '中考英语作文')
    query.skip(count)
    querys = query.find()
    size = len(querys)
    if size == 0:
        return

    for data in querys:
        print(data.get('title'))
        data.set('type_id','1003')
        data.save()


if __name__ == '__main__':
    for i in range(0,18):
        print(i*100)
        is_exit(i*100)
        # is_exit(100)






