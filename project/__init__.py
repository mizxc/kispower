# -*- coding: utf-8 -*-
# @CTime   : 2019-12-20
# @MTime   :
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com
# @File    : __init__.py

from project.app.admin import bpAdmin
from project.app.auth import bpAuth
from project.app.home import bpHome

def bpRegister(app):
    """
    蓝图
    """
    app.register_blueprint(bpAdmin, url_prefix="/kadmin")
    app.register_blueprint(bpAuth, url_prefix="/kauth")
    app.register_blueprint(bpHome, url_prefix="/")
