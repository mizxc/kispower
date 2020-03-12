# -*- coding: utf-8 -*-
# @Time    : 2019-12-20
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

from flask_mongoengine import MongoEngine
from flask_login import LoginManager

db = MongoEngine()
loginManager = LoginManager()
