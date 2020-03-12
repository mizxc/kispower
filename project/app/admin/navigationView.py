# -*- coding: utf-8 -*-
# @Time    : 2019-12-20
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

import os
from flask import current_app, request, flash, render_template, redirect, url_for
from flask_login import login_required, current_user
from . import bpAdmin
from project.common.dataPreprocess import strLength
from project.model.navigation import *
from project.common.filePreprocess import allowedImage, creatFileName, allowedFileSize, removeFile

@bpAdmin.route("/navigationColumn")
@login_required
def navigationColumn():
    ns = Navigation.objects.order_by('+number')
    return render_template('admin/navigationColumn.html',ns=ns)

@bpAdmin.route("/navigationColumnAdd", methods=['POST'])
@login_required
def navigationColumnAdd():
    column = request.form['column']
    introduction = request.form['introduction']

    if not strLength(column,1,60):
        flash(u'请输入60个字符内的栏目名称！')
        return redirect(url_for('admin.navigationColumn'))

    if introduction and not strLength(introduction,1,1000):
        flash(u'请输入1000个字符内的栏目介绍！')
        return redirect(url_for('admin.navigationColumn'))

    n = Navigation()
    n.column = column
    n.number = Navigation.objects.count()+1
    if introduction:n.introduction=introduction
    n.save()
    flash(u'栏目添加成功！')
    return redirect(url_for('admin.navigationColumn'))

@bpAdmin.route("/navigationColumnEdit/<id>", methods=['GET','POST'])
@login_required
def navigationColumnEdit(id):
    n = Navigation.objects(id=id).first()
    if request.method == 'GET':
        return render_template('admin/navigationColumnEdit.html',n=n)
    if request.method == 'POST':
        column = request.form['column']
        introduction = request.form['introduction']

        if not strLength(column,1,60):
            flash(u'请输入60个字符内的栏目名称！')
            return redirect(url_for('admin.navigationColumn'))
        if introduction and not strLength(introduction,1,1000):
            flash(u'请输入1000个字符内的栏目介绍！')
            return redirect(url_for('admin.navigationColumn'))

        n.column = column
        if introduction:n.introduction=introduction
        else:n.introduction=None
        n.save()
        flash(u'栏目修改成功！')
        return redirect(url_for('admin.navigationColumn'))

@bpAdmin.route("/navigationColumnNumberChange/<number>/<direction>", methods=['GET'])
@login_required
def navigationColumnNumberChange(number, direction):
    current = Navigation.objects(number=int(number)).first()
    currentNumber = int(number)
    if direction == 'up':
        next = Navigation.objects(number=int(number)-1).first()
    if direction == 'down':
        next = Navigation.objects(number=int(number)+1).first()
    nextNumber = next.number

    current.number = nextNumber
    current.save()
    next.number = currentNumber
    next.save()
    return redirect(url_for('admin.navigationColumn'))

@bpAdmin.route("/navigationColumnDelete/<id>", methods=['GET'])
@login_required
def navigationColumnDelete(id):
    n = Navigation.objects(id=id).first()
    if len(n.webs)>0:
        flash(u'栏目下有网站，不能删除，先删除网站再删除栏目！')
        return redirect(url_for('admin.navigationColumn'))

    n.delete()
    #删除后，剩下的重新排编号
    ns = Navigation.objects.order_by('+number')
    for index, n in enumerate(ns):
        n.number = index+1
        n.save()
    flash(u'栏目删除成功！')
    return redirect(url_for('admin.navigationColumn'))

@bpAdmin.route("/navigationColumnManage/<id>")
@login_required
def navigationColumnManage(id):
    n = Navigation.objects(id=id).first()
    return render_template('admin/navigationColumnManage.html',n=n)

@bpAdmin.route("/navigationWebAdd/<id>", methods=['POST'])
@login_required
def navigationWebAdd(id):
    n = Navigation.objects(id=id).first()

    webName = request.form['webName']
    url = request.form['url']
    icon = request.files.get('img')
    introduction = request.form['introduction']

    if not strLength(webName,1,60):
        flash(u'请输入60个字符内的网站名称！')
        return redirect(url_for('admin.navigationColumnManage', id=id))
    if not strLength(url,1,1000):
        flash(u'请输入1000个字符内的网站url！')
        return redirect(url_for('admin.navigationColumnManage', id=id))
    if not url.startswith('http'):
        flash(u'url开头请带上http://或者https://')
        return redirect(url_for('admin.navigationColumnManage', id=id))
    if introduction and not strLength(introduction,1,1000):
        flash(u'请输入1000个字符内的栏目介绍！')
        return redirect(url_for('admin.navigationColumnManage', id=id))

    #其他字段判断完再判断图片上传
    iconPath = None
    if icon and allowedImage(icon.filename):
        if allowedFileSize(len(icon.read()), 1):
            icon.seek(0)
            fileName = creatFileName(current_user.id, icon.filename)
            icon.save(os.path.join(current_app.config['UPLOAD_WEBICON_PATH'], fileName))
            iconPath = current_app.config['UPLOAD_PATH_WEBICON_FOR_DB'] + '/' + fileName
        else:
            flash(u"请上传小于1M的图片！")
            return redirect(url_for('admin.navigationColumnManage', id=id))

    w = Web()
    w.webName = webName
    w.url = url
    if introduction:w.introduction=introduction
    if iconPath:w.icon=iconPath
    n.webs.append(w)
    n.save()
    flash(u'网站添加成功！')
    return redirect(url_for('admin.navigationColumnManage',id=id))

@bpAdmin.route("/navigationWebEdit/<id>/<number>", methods=['GET','POST'])
@login_required
def navigationWebEdit(id,number):
    number = int(number)
    n = Navigation.objects(id=id).first()
    w = n.webs[number]

    if request.method == 'GET':
        return render_template('admin/navigationWebEdit.html',n=n,w=w,number=number)

    if request.method == 'POST':
        webName = request.form['webName']
        url = request.form['url']
        icon = request.files.get('img')
        introduction = request.form['introduction']

        if not strLength(webName,1,60):
            flash(u'请输入60个字符内的网站名称！')
            return redirect(url_for('admin.navigationColumnManage', id=id))
        if not strLength(url,1,1000):
            flash(u'请输入1000个字符内的网站url！')
            return redirect(url_for('admin.navigationColumnManage', id=id))
        if not url.startswith('http'):
            flash(u'url开头请带上http://或者https://')
            return redirect(url_for('admin.navigationColumnManage', id=id))
        if introduction and not strLength(introduction,1,1000):
            flash(u'请输入1000个字符内的栏目介绍！')
            return redirect(url_for('admin.navigationColumnManage', id=id))

        #其他字段判断完再判断图片上传
        iconPath = None
        if icon and allowedImage(icon.filename):
            if allowedFileSize(len(icon.read()), 1):
                icon.seek(0)
                fileName = creatFileName(current_user.id, icon.filename)
                icon.save(os.path.join(current_app.config['UPLOAD_WEBICON_PATH'], fileName))
                iconPath = current_app.config['UPLOAD_PATH_WEBICON_FOR_DB'] + '/' + fileName
                if w.icon:
                    #删除以前的图片
                    removeFile(os.path.join(current_app.config['STATIC_PATH'], w.icon))
            else:
                flash(u"请上传小于1M的图片！")
                return redirect(url_for('admin.navigationColumnManage', id=id))

        w.webName = webName
        w.url = url
        if introduction:w.introduction=introduction
        else:w.introduction=None
        if iconPath:w.icon=iconPath
        n.webs[number]=w
        n.save()
        flash(u'网站修改成功！')
        return redirect(url_for('admin.navigationColumnManage',id=id))

@bpAdmin.route("/navigationWebNumberChange/<id>/<number>/<direction>", methods=['GET'])
@login_required
def navigationWebNumberChange(id,number, direction):
    number = int(number)
    n = Navigation.objects(id=id).first()

    current = n.webs[number]
    if direction == 'up':
        next = n.webs[number-1]
        n.webs[number] = next
        n.webs[number - 1] = current
    if direction == 'down':
        next = n.webs[number+1]
        n.webs[number] = next
        n.webs[number + 1] = current
    n.save()
    return redirect(url_for('admin.navigationColumnManage', id=id))

@bpAdmin.route("/navigationWebDelete/<id>/<number>", methods=['GET'])
@login_required
def navigationWebDelete(id,number):
    number = int(number)
    n = Navigation.objects(id=id).first()
    w = n.webs[number]
    #删除图标，先判断是否有图标
    if w.icon:
        removeFile(os.path.join(current_app.config['STATIC_PATH'], w.icon))
    n.webs.remove(w)
    n.save()
    flash(u'网站删除成功！')
    return redirect(url_for('admin.navigationColumnManage', id=id))



