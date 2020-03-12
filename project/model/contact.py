# -*- coding: utf-8 -*-
# @Time    : 2019-12-27
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

from mongoengine import *

class contactMessage(Document):
    name = StringField(max_length=30, required=True)
    email = StringField(required=True)
    message = StringField(max_length=2000)
    at = StringField(required=True)
    processed = BooleanField(default=False)


