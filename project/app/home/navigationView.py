# -*- coding: utf-8 -*-
# @Time    : 2019-12-20
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

import os
from flask import current_app, request, flash, render_template, redirect, url_for
from flask_login import login_required, current_user
from . import bpHome
from project.common.dataPreprocess import strLength
from project.model.navigation import *
from project.common.filePreprocess import allowedImage, creatFileName, allowedFileSize, removeFile

@bpHome.route("/navigation")
def navigation():
    ns = Navigation.objects.order_by('+number')
    return render_template('%s/navigation.html' % current_user.getCustom()['homeTemplate'],
                           ns=ns,mark='navigation')



