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
    query = Query('Reading')
    # query.equal_to('category', 'shuangyu_reading')
    query.equal_to('source_name','酷悠双语网')
    print query.count()


if __name__ == '__main__':
    is_exit(0)






