# -*- coding:utf-8 -*-

import hashlib

''' 绘本森林公用参数'''

#host="http://192.168.1.216:8686/"
host="https://m.xueduoduo.com"
appType='ipad'
clientPackage='com.xueduoduo.xinyunketang'
clientVersion='7.4'
version='1.0'
landIp='123'
systemVersion='12.0.1'

base_para={'appType':'ipad','clientPackage':'com.xueduoduo.xinyunketang','clientVersion':'7.4','version':'1.0','landIp':'123','systemVersion':'12.3.1'}


'''绘本森林md5加密'''
def passWords(passWord):

    md=hashlib.md5()

    str1=passWord.encode(encoding=('utf-8'))

    md.update(str1)

    return  md.hexdigest()
