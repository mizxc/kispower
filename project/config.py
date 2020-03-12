# -*- coding: utf-8 -*-
# @Time    : 2019-12-20
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

import os
from datetime import timedelta

class BaseConfig:
    """
    配置基类
    设置环境
    export FLASK_ENV=development
    export FLASK_ENV=production
    """
    #_____________________________________________________________________
    VERSION = 'v2.5'
    WEBSITE = '127.0.0.1'
    WEBSITE_KISPOWER = 'http://www.kispower.cn'
    URL_FEEDBACK = '%s/private/feedbackAdd' % WEBSITE_KISPOWER
    URL_VERSION = '%s/private/redirectToVersion' % WEBSITE_KISPOWER #版本号目录
    URL_USERGUIDE = '%s/private/redirectToGuide' % WEBSITE_KISPOWER #系统操作手册
    #提交到共享知识库，必须要终端管理有该客户信息
    URL_KSHARE_POST = '%s/private/knowledgeBasePostKShare' % WEBSITE_KISPOWER #提交到共享知识库
    URL_KSHARE_DELETE = '%s/private/knowledgeBaseDeleteKShare' % WEBSITE_KISPOWER #从共享知识库删除
    # _____________________________________________________________________

    SECRET_KEY = 'LSKDJFIWEL3O49234-LSKDJFI2KDF-SLKFJ2204'  # session加密
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)  # 设置session过期时间

    # mongodb
    DBHOST = '127.0.0.1'
    DBPORT = 27017
    DBNAME = 'kispower'

    #项目根目录
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    #项目static目录
    STATIC_PATH = os.path.join(BASE_DIR,'static')
    # 模板主题目录
    TPMPLATE_PATH = os.path.join(BASE_DIR, 'static/theme')
    TPMPLATE_PATH = 'static/theme'
    # 随机图片库
    RANDOM_IMAGE_PATH = 'static/local/images/random'
    # 默认上传文件路径
    UPLOAD_PATH_FOR_DB = '_upload'
    UPLOAD_PATH = os.path.join(STATIC_PATH,UPLOAD_PATH_FOR_DB)
    # 网站图标上传路径
    UPLOAD_PATH_WEBICON_FOR_DB = '_upload/webIcon'
    UPLOAD_WEBICON_PATH = os.path.join(STATIC_PATH, UPLOAD_PATH_WEBICON_FOR_DB)
    #相册上传路径
    UPLOAD_PATH_PHOTOALBUM_FOR_DB = '_upload/photoAlbum'
    UPLOAD_PHOTOALBUM_PATH = os.path.join(STATIC_PATH, UPLOAD_PATH_PHOTOALBUM_FOR_DB)
    #数据备份路径
    BACKUP_PATH = os.path.abspath(os.path.join(BASE_DIR, "../backup"))
    #日志存放路径
    LOGS_PATH = os.path.abspath(os.path.join(BASE_DIR, "../logs"))

    #计划任务级别
    PLAN_LEVEL = {
        "L1":u"紧急重要",
        "L2":u"紧急不重要",
        "L3":u"重要不紧急",
        "L4":u"不重要不紧急"
    }

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(BaseConfig):
    """
    开发环境
    """
    DEBUG = True

class ProductionConfig(BaseConfig):
    """生产环境"""
    DEBUG = False

configObj = {
        'production': ProductionConfig,
        'development': DevelopmentConfig,
        'default': DevelopmentConfig
    }

def getEnv():
    return os.environ.get('FLASK_ENV') if os.environ.get('FLASK_ENV') else "production"
