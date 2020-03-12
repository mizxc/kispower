# -*- coding: utf-8 -*-
# @Time    : 2020-01-20
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

import os
from flask import current_app, request, flash, render_template, redirect, url_for, jsonify
from flask_login import login_required, current_user
from . import bpAdmin
from project.model.contact import contactMessage
from project.common.filePreprocess import allowedImage, creatFileName, allowedFileSize, removeFile
from project.common.dataPreprocess import strLength

@bpAdmin.route("/contact")
@login_required
def contact():
    messages = contactMessage.objects.order_by('-id')
    return render_template('admin/contact.html',messages=messages)

@bpAdmin.route("/contactDelete/<id>", methods=['POST'])
@login_required
def contactDelete(id):
    c = contactMessage.objects(id=id).first()
    c.delete()
    return jsonify({'status':True,'info':u'删除成功！'})

@bpAdmin.route("/contactProcessed/<id>", methods=['POST'])
@login_required
def contactProcessed(id):
    c = contactMessage.objects(id=id).first()
    if c.processed == True:
        c.processed = False
    else:
        c.processed = True
    c.save()
    return jsonify({'status':True,'info':u'处理成功！'})


