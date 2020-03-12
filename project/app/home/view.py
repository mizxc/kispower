# -*- coding: utf-8 -*-
# @Time    : 2019-12-21
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

from flask import current_app, request, flash, render_template, redirect, url_for,jsonify
from flask_login import current_user
from . import bpHome
from project.common.regular import reEmail
from project.common.dataPreprocess import strLength, getStrTime
from project.model.contact import contactMessage
from project.model.blog import *
from project.common.dataPreprocess import getPagingParameters

@bpHome.route("/", methods=['GET', 'POST'])
@bpHome.route("/<page>", methods=['GET', 'POST'])
def index(page=0):
    tpl = current_user.getCustom()['homeTemplate']
    if 'lifeleck' in tpl or '__terminal' in tpl:
        page = int(page)
        sk = getPagingParameters(page,11)
        ps = Post.objects().order_by('-isTop', '-id')[sk[0]:sk[1]]
        return render_template('%s/index.html' % current_user.getCustom()['homeTemplate'],
                               ps=ps, page=page,mark='index')
    else:
        return render_template('%s/index.html' % current_user.getCustom()['homeTemplate'],
                               mark='index')

@bpHome.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('%s/about.html' % current_user.getCustom()['homeTemplate'],
                           mark='about')

@bpHome.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('%s/contact.html' % current_user.getCustom()['homeTemplate'],
                               mark='contact')
    elif request.method == 'POST':
        name = request.form['name']
        if not strLength(name,1,20):
            return jsonify({'status':False,'info':u'请输入20个字符内的名字'})
        email = request.form['email']
        if not reEmail(email):
            return jsonify({'status': False, 'info': u'请输入正确的邮箱'})
        message = request.form['message']
        if not strLength(message,1,1000):
            return jsonify({'status':False,'info':u'请输入1000个字符内的消息'})
        c = contactMessage()
        c.name = name
        c.email = email
        c.message = message
        c.at = getStrTime()
        c.save()
        return jsonify({'status': True, 'info': u'提交成功！'})



