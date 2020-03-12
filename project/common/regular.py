# -*- coding: utf-8 -*-
# @Time    : 2019-12-22
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

import re

def reEmail(str):
    return re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', str)


if __name__ == '__main__':
    print (reEmail(''))
    print (len('12222'))