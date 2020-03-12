# -*- coding: utf-8 -*-
# @Time    : 2019-12-21
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

from flask import Blueprint
bpAuth = Blueprint("auth",__name__)

from .view import *