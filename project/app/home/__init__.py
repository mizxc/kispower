# -*- coding: utf-8 -*-
# @Time    : 2019-12-21
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

from flask import Blueprint
bpHome = Blueprint("home",__name__)

from .view import *
from .navigationView import *
from .blogView import *
from .photoView import *
from .kshareView import *