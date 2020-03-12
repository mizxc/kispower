# -*- coding: utf-8 -*-
# @Time    : 2019-12-21
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

import os
import random
from mongoengine import *
from flask_login import UserMixin, AnonymousUserMixin
from project.model.blog import *
from project.model.photoAlbum import *
from project.config import BaseConfig

USER_CUSTOM = {
    'webName': 'kispower',
    'webIntro': u'好用的知识管理工具',
    'webKeywords':u'kispower 知识管理 学习工具',
    'favicon': 'local/images/favicon.png',
    'logo': 'local/images/logo.png',
    'copyright':u'Copyright © 2020 <a href="http://www.kispower.cn">Kispower</a> All rights reserved 粤ICP备xxxxxx号',
    'statisticalCode':'',
    'commentCode':'',
    'homeTemplate': 'theme/default',
    'slide':[
        ['local/images/slide1.jpg','kispower','个人知识管理系统','http://www.kispower.com'],
        ['local/images/slide2.jpg','kispower','最好用的知识管理系统','http://www.kispower.com'],
        ['local/images/slide3.jpg','kispower','知识管理+时间管理','http://www.kispower.com'],
        ['local/images/slide4.jpg','kispower','个人知识分享网站','http://www.kispower.com'],
        ['local/images/slide5.jpg','kispower','个人网络工作室','http://www.kispower.com']
    ],
    'tags':{},
    'weixin':'local/images/weixin.jpg',
    'weibo':'https://weibo.com/p/1005056368574508',
    'dailyTasks':[
        ['L1',u'请点击：日常任务管理，添加常用任务'],
        ['L2',u'如果不需要可以删除全部日常任务']
    ]
}

class CommonUserMethod:
    def getRandomImage(self):
        randomImagePath = os.path.join(BaseConfig.BASE_DIR, BaseConfig.RANDOM_IMAGE_PATH)
        images = os.listdir(randomImagePath)
        return '/%s/%s' % (BaseConfig.RANDOM_IMAGE_PATH,random.choice(images))

    def getBlogColumn(self):
        return Column.objects.order_by('+number')

    def getRecentPost(self):
        return Post.objects.order_by('-id')[:5]

    def getHotPost(self):
        return Post.objects.order_by('-pv')[:5]

    def getPrevAndNextPost(self,id):
        ps = Post.objects
        prev = None
        next = None
        for index, p in enumerate(ps):
            if p.id == id:
                if index!=0:prev = ps[index-1]
                if index+1<ps.count():next = ps[index+1]
        return (prev,next)

    def getPhotoAlbum(self):
        return Album.objects(isShow=True).order_by('+number')

    def getRecentPhoto(self):
        return Photo.objects().order_by('-id')[:12]

    def getPhotoByAlbum(self,albumId):
        album = Album.objects(id=albumId).first()
        return Photo.objects(album=album).order_by('-id').first()


class User(Document, UserMixin, CommonUserMethod):
    userName = StringField(max_length=60, required=True)
    password = StringField(max_length=128, required=True)
    email = StringField(max_length=60, required=True)
    icon = StringField(max_length=1000, default='local/images/face.jpg')
    aboutMe = StringField(max_length=15000)
    custom = DictField(default=USER_CUSTOM)

    def get_id(self):
        return str(self.id)

    #认证用户与非认证用户都返回管理员用户的网站设置信息
    def getCustom(self):
        custom = self.custom
        custom['userName'] = self.userName
        custom['icon'] = self.icon
        custom['email'] = self.email.replace('@',u'【请替换成@】')
        custom['aboutMe'] = self.aboutMe
        return custom

class AnonymousUser(AnonymousUserMixin, CommonUserMethod):
    def is_administrator(self):
        return False

    def getCustom(self):
        user = User.objects.first()
        if user:return user.getCustom()
        else:return USER_CUSTOM



