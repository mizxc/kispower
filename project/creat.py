# -*- coding: utf-8 -*-
# @Time    : 2019-12-20
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

from flask import Flask
from project import bpRegister
from project.register import configRegister, dbRegister, loginRegister


def create_app():
    """
    创建flask实例
    """
    app = Flask(__name__, template_folder='templates',
                static_folder='static')
    configRegister(app)
    dbRegister(app)
    bpRegister(app)
    loginRegister(app)
    return app
