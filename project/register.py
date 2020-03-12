# -*- coding: utf-8 -*-
# @CTime   : 2019-12-20
# @MTime   :
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com
# @File    : __init__.py

import os
from project.extension import db, loginManager
from project.config import *
from project.model.user import User, AnonymousUser

def configRegister(app):
    """
    注册配置
    设置环境
    export FLASK_ENV=development
    export FLASK_ENV=production
    """
    env = getEnv()
    app.config.from_object(configObj[env])  # 环境配置
    configObj[env].init_app(app)

def dbRegister(app):
    """
    注册数据库
    """
    env = getEnv()
    app.config['MONGODB_SETTINGS'] = {
        'db': configObj[env].DBNAME,
        'host': configObj[env].DBHOST,
        'port': configObj[env].DBPORT
    }
    db.init_app(app)

def loginRegister(app):
    """
    注册登陆管理
    """
    loginManager.session_protection = 'strong'
    loginManager.login_view = 'auth.userLogin'
    loginManager.anonymous_user = AnonymousUser
    loginManager.init_app(app)

    @loginManager.user_loader
    def load_user(id):
        return User.objects(id = id).first()
