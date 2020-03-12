# -*- coding: utf-8 -*-
# @Time    : 2019-12-20
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

from flask import Blueprint
bpAdmin = Blueprint("admin",__name__)

from .view import *
from .userView import *
from .navigationView import *
from .timeManagementView import *
from .photoAlbumView import *
from .blogView import *
from .kmView import *
from .webView import *
from .slideView import *
from .contactView import *