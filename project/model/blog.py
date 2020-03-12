# -*- coding: utf-8 -*-
# @Time    : 2019-12-27
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

from mongoengine import *
import datetime

class Column(Document):
    title = StringField(max_length=30, required=True)
    number = IntField(required=True)
    introduction = StringField(max_length=100)
    postCount = IntField(required=True,default=0)

class Post(Document):
    column = ReferenceField(Column)
    title = StringField(max_length=100)
    tags = ListField(StringField(),default=[])
    tagSource = StringField(max_length=60)
    video = StringField(max_length=500)
    content = StringField(max_length=50000)
    lead = StringField(max_length=300)
    cover = StringField(max_length=500)
    writeTime = StringField(max_length=100)
    pv = IntField(required=True,default=0)
    isTop = BooleanField(default=False)

    meta = {'indexes': [
        {'fields': ['$title', '$tags',"$content"],
         'default_language': 'english',
         'weights': {'title': 10, 'tags':6,'content': 2}
         }
    ]}


