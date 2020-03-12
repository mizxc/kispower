# -*- coding: utf-8 -*-
# @Time    : 2019-12-22
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

import os
import time

def allowedImage(fileName):
    """
    判读是否是允许的图片类型
    """
    ALLOWED = ['jpg', 'JPG','jpeg','JPEG','png','PNG', 'gif', 'GIF','ico','svg']
    return '.' in fileName and fileName.rsplit('.', 1)[1] in ALLOWED

def creatFileName(id,fileName):
    """
    filename=用户id+时间戳+后缀
    """
    return fileName.rsplit('.', 1)[0] + str(id) + str(time.time()) + '.' + fileName.rsplit('.', 1)[1]

def allowedFileSize(size,m):
    """
    允许的图片大小：1M=1048576字节
    """
    return size <= 1048578*m

def removeFile(path):
    try:
        os.remove(path)
    except:
        pass

def writeLog(path,info):
    """
    写日志文件，如果文件超过10M，覆盖文件
    """
    #判断是否存在文件,不存在创建
    if not os.path.exists(path):
        with open(path, 'w') as wf:
            wf.write('%s\n' % info)
    else:
        size = os.path.getsize(path)
        if (size/1000000) > 10.0:
            with open(path, 'w') as wf:
                wf.write('%s\n' % info)
        else:
            with open(path, 'a') as wf:
                wf.write('%s\n' % info)
