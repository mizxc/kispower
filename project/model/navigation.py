# -*- coding: utf-8 -*-
# @Time    : 2019-12-23
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

from mongoengine import *

class Web(EmbeddedDocument):
    webName = StringField(max_length=60, required=True)
    url = StringField(max_length=1000, required=True)
    icon = StringField(max_length=1000)
    introduction = StringField(max_length=1000)

class Navigation(Document):
    column = StringField(max_length=60, required=True)
    number = IntField(required=True)
    introduction = StringField(max_length=1000)
    webs = ListField(EmbeddedDocumentField(Web))


