#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import sys
import thread

import pickle

if __name__ == '__main__':
    print '---main---'
    number = 1
    while True:
        print 'Start task:spider' + time.strftime('%Y-%m-%d %X', time.localtime())
        print '----------'
        try:
            execfile('Execfile.py')
            if number == 1:
                file = open('log.txt', 'wb')
                pickle.dump(time.strftime('%Y-%m-%d %X', time.localtime()), file)
                file.close()

            file = open('log.txt', 'a')
            pickle.dump(time.strftime('%Y-%m-%d %X', time.localtime()), file)
            file.close()
        except:
            print 'except'
        number += 1
        time.sleep(3600)


