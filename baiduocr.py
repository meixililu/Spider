#!/usr/bin/env python
# -*- coding:utf-8 -*-
from aip import AipOcr

# 定义常量
APP_ID = '9470738'
API_KEY = 'GNBFfzUk2F9fzS109aTIiIDG'
SECRET_KEY = '6cuMEl0DPCQfeBhaiEvQq6koNFBHzw3C'

# 读取图片
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 初始化ApiOcr对象
aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

# 调用通用文字识别接口
result = aipOcr.basicGeneral(get_file_content('tran_temp.jpg'))

for item in result['words_result']:
    print item['words']