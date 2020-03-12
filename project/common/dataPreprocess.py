# -*- coding: utf-8 -*-
# @Time    : 2019-12-23
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com


import re
import time
import datetime
from bs4 import BeautifulSoup

def strLength(str,min,max):
    """
    判读数据长度
    """
    return len(str)>=min and len(str)<=max

#获取标签数组，同时清除空字符串,清除相同tag
def getTagsFormStrTag(str):
    array = str.strip().split(' ')
    while "" in array:
        array.remove("")
    return list(set(array))

#_______________________________________________
# datetime时间转为字符串
def getStrTime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def datetimeToStr(datetime1):
    str1 = datetime1.strftime('%Y-%m-%d %H:%M:%S')
    return str1

# 字符串时间转为时间戳
def strToTimestamp(str1):
    Unixtime = time.mktime(time.strptime(str1, '%Y-%m-%d %H:%M:%S'))
    return Unixtime

# datetime时间转为时间戳
def datetimeToTimestamp(dt1):
    Unixtime = time.mktime(time.strptime(dt1.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))
    return Unixtime

# 时间戳转为datetime时间
def timestampToDatetime(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp)
    return dt

# uinx时间戳转换为本地时间
def timestampToLocaltime(datetime1):
    Localtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(datetime1))
    return Localtime

# 字符串时间转datetime
def strToDatetime(str1):
    return timestampToDatetime(strToTimestamp(str1))
#_______________________________________________

#mongoengine 分页获取
def getPagingParameters(page,count=10):
    #默认分页：10
    page = int(page)
    return [page*count,(page+1)*count]

#获取文章html代码，导语/cover
def getLeadAndCover(s):
    s = '<div>%s</div>' % s
    ret = [None,None]
    bs = BeautifulSoup(s, "html.parser")
    ret[0] = bs.div.get_text()[:200] + '...'
    img = bs.find_all('img')
    if img:ret[1]=img[0].get('src')
    return ret


if __name__ == '__main__':
    a = ' sdf sdf   sdf sdf sfwefgw sfd wef sd   sd d  fewef '
    ret = getTagsFormStrTag(a)
    print (ret)