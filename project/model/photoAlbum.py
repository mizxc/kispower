# -*- coding: utf-8 -*-
# @Time    : 2019-12-27
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

from mongoengine import *

class Album(Document):
    title = StringField(max_length=60, required=True)
    number = IntField(required=True)
    isShow = BooleanField(default=True)  # 是否显示
    introduction = StringField(max_length=1000)
    photoCount = IntField(required=True,default=0)

class Photo(Document):
    title = StringField(max_length=60)
    introduction = StringField(max_length=1000)
    path = StringField(max_length=1000)
    album = ReferenceField(Album)
    isTop = BooleanField(default=False)


