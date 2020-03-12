# -*- coding: utf-8 -*-
# @Time    : 2019-12-20
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

import os
from flask import current_app, request, flash, render_template, redirect, url_for
from flask_login import login_required, current_user
from . import bpHome
from project.model.blog import *
from project.common.dataPreprocess import getPagingParameters

@bpHome.route("/blog")
@bpHome.route("/blog/<page>")
def blog(page=0,columnId=None,tag=None):
    page = int(page)
    sk = getPagingParameters(page)
    ps = Post.objects().order_by('-isTop','-id')[sk[0]:sk[1]]
    return render_template('%s/blog.html' % current_user.getCustom()['homeTemplate'],
                           ps=ps,page=page,mark='blog')

@bpHome.route("/blogColumn/<columnId>")
@bpHome.route("/blogColumn/<columnId>/<page>")
def blogColumn(columnId,page=0):
    page = int(page)
    sk = getPagingParameters(page)
    c = Column.objects(id=columnId).first()
    ps = Post.objects(column=c).order_by('-isTop', '-id')[sk[0]:sk[1]]
    return render_template('%s/blog.html' % current_user.getCustom()['homeTemplate'],
                           ps=ps,page=page,mark='blog',c=c)

@bpHome.route("/blogTag/<tag>")
@bpHome.route("/blogTag/<tag>/<page>")
def blogTag(tag,page=0):
    page = int(page)
    sk = getPagingParameters(page)
    ps = Post.objects(tags=tag).order_by('-isTop', '-id')[sk[0]:sk[1]]
    return render_template('%s/blog.html' % current_user.getCustom()['homeTemplate'],
                           ps=ps,page=page,mark='blog',tag=tag)

@bpHome.route("/blogSearch",methods=['GET','POST'])
@bpHome.route("/blogSearch/<search>/<page>",methods=['GET','POST'])
def blogSearch(search=None,page=0):
    if not search:
        search = request.form['search']
    page = int(page)
    sk = getPagingParameters(page)
    ps = Post.objects.search_text(search)[sk[0]:sk[1]]
    return render_template('%s/blog.html' % current_user.getCustom()['homeTemplate'],
                           ps=ps,page=page,mark='blog',search=search)

@bpHome.route("/blogShow/<id>")
def blogShow(id):
    p = Post.objects(id=id).first()
    p.pv += 1
    p.save()
    return render_template('%s/blogShow.html' % current_user.getCustom()['homeTemplate'],
                           p=p,mark='blog')


