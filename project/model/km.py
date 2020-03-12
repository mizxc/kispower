# -*- coding: utf-8 -*-
# @Time    : 2019-12-29
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

import requests
from mongoengine import *
from project.common.dataPreprocess import getStrTime

class KClass(Document):
    title = StringField(max_length=60, required=True)
    introduction = StringField(max_length=1000)
    versions = ListField(DictField())
    k = DictField()
    isTop = BooleanField(default=False)

class KShare(Document):
    title = StringField(max_length=60)
    tag = ListField()
    introduction = StringField(max_length=10000)
    introductionHtml = StringField(max_length=15000)
    source = StringField(max_length=1000)#记录节点是从哪里分享来的（kClass.id+分享根节点id）
    shareTime = StringField(max_length=100)
    pv = IntField(required=True, default=0)
    k = DictField()

    def postKShareToBase(self,tag,author,website,postUrl):
        postData = {
            "website":website,
            "title":self.title,
            "tag":tag,
            "introduction":self.introduction,
            "author":author,
            "source":website+self.source,
            "shareTime":self.shareTime,
            "url":'%s/kispowerKShareShow/%s' % (website,self.id),
        }
        requests.post(postUrl, data=postData, timeout=10)

    def deleteKShareFromBase(self,website,postUrl):
        requests.post(postUrl, data={"website":website,"source":website+self.source}, timeout=10)

def creatNewKClass(title,author):
    data = {
        "meta": {
            "name": title,
            "author": author,
            "version": 1.0,
            "saveTime":getStrTime(),
            "backgroundColor": "#ffffff",
            "lineColor": "#555",
            "displayMode": "side",
        },
        "format": "node_tree",
        "data": {
            "id": "root",
            "topic": title,
            "background-color": "#ff2121",
            "foreground-color": "#ffffff",
            "topicType": "ordinary",
            "children": [],
        }
    }
    return data
