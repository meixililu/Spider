#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys

import traceback
import time
if __name__ == '__main__':
    try:
        print 'Start task:spider' + time.strftime('%Y-%m-%d %X', time.localtime())
        print 'execfile------iciba_study_spider.py'
        execfile('iciba_study_spider.py')
    except:
        print traceback.format_exc()

    try:
        print 'execfile------jianghu_reading_spider.py'
        execfile('jianghu_reading_spider.py')
    except:
        print traceback.format_exc()

    try:
        print 'execfile------yingyu_com_chilren_story_spider.py'
        execfile('yingyu_com_chilren_story_spider.py')
    except:
        print traceback.format_exc()

    try:
        print 'execfile------yingyu_com_chilren_spoken_english_spider.py'
        execfile('yingyu_com_chilren_spoken_english_spider.py')
    except:
        print traceback.format_exc()

    try:
        print 'execfile------adreep_spider.py'
        execfile('adreep_spider.py')
    except:
        print traceback.format_exc()

    try:
        print 'execfile------Henxingwang_composition_spider.py'
        execfile('Henxingwang_composition_spider.py')
    except:
        print traceback.format_exc()

    try:
        print 'execfile------Henxingwang_listening_spider.py'
        execfile('Henxingwang_listening_spider.py')
    except:
        print traceback.format_exc()

    try:
        print 'execfile------Henxingwang_word_spider.py'
        execfile('Henxingwang_word_spider.py')
    except:
        print traceback.format_exc()

    try:
        print 'execfile------Henxingwang_yuedulijie_spider.py'
        execfile('Henxingwang_yuedulijie_spider.py')
    except:
        print traceback.format_exc()

    try:
        print 'execfile------en8848_story_spider.py'
        execfile('en8848_story_spider.py')
    except:
        print traceback.format_exc()

    # try:
    #     print 'execfile------cuyoo_spider.py'
    #     execfile('cuyoo_spider.py')
    # except:
    #     print traceback.format_exc()











