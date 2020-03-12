# -*- coding: utf-8 -*-
# @Time    : 2020-01-20
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

import os
from flask import current_app, request, flash, render_template, redirect, url_for, jsonify
from flask_login import login_required, current_user
from . import bpAdmin
from project.common.filePreprocess import allowedImage, creatFileName, allowedFileSize, removeFile
from project.common.dataPreprocess import strLength

@bpAdmin.route("/webSetting")
@login_required
def webSetting():
    return render_template('admin/webSetting.html')

@bpAdmin.route("/setWebInfo", methods=['POST'])
@login_required
def setWebInfo():
    webName = request.form['webName']
    webIntro = request.form['webIntro']
    webKeywords = request.form['webKeywords']
    if not strLength(webName,1,32):
        flash(u"网站名：最多16个汉字")
        return redirect(url_for('admin.webSetting'))
    if not strLength(webIntro,1,256):
        flash(u"网站简介：最多128个汉字")
        return redirect(url_for('admin.webSetting'))
    if not strLength(webKeywords,1,128):
        flash(u"网站关键词：最多64个汉字")
        return redirect(url_for('admin.webSetting'))

    current_user.custom['webName'] = webName
    current_user.custom['webIntro'] = webIntro
    current_user.custom['webKeywords'] = webKeywords
    current_user.save()
    flash(u"信息修改成功！")
    return redirect(url_for('admin.webSetting'))

@bpAdmin.route("/setWebLogo", methods=['POST'])
@login_required
def setWebLogo():
    img = request.files.get('img')
    if not allowedFileSize(len(img.read()),1):
        flash(u"请上传小于1M的图片！")
        return redirect(url_for('admin.webSetting'))
    #文件read后，要重样把指针定位到开头
    img.seek(0)
    if img and allowedImage(img.filename):
        try:
            fileName = creatFileName(current_user.id, img.filename)
            img.save(os.path.join(current_app.config['UPLOAD_PATH'], fileName))
            if 'local/images/' not in current_user.custom['logo']:
                #删除以前的图片
                removeFile(os.path.join(current_app.config['STATIC_PATH'], current_user.custom['logo']))
            current_user.custom['logo'] = current_app.config['UPLOAD_PATH_FOR_DB'] + '/' + fileName
            current_user.save()
            flash(u"logo修改成功！")
        except:
            flash(u"图片上传失败！")
    else:
        flash(u"请上传png/jpg/gif图片！")
    return redirect(url_for('admin.webSetting'))

@bpAdmin.route("/setWebFavicon", methods=['POST'])
@login_required
def setWebFavicon():
    img = request.files.get('img')
    if not allowedFileSize(len(img.read()),1):
        flash(u"请上传小于1M的图片！")
        return redirect(url_for('admin.webSetting'))
    #文件read后，要重样把指针定位到开头
    img.seek(0)
    if img and allowedImage(img.filename):
        try:
            fileName = creatFileName(current_user.id, img.filename)
            img.save(os.path.join(current_app.config['UPLOAD_PATH'], fileName))
            if 'local/images/' not in current_user.custom['favicon']:
                #删除以前的图片
                removeFile(os.path.join(current_app.config['STATIC_PATH'], current_user.custom['favicon']))
            current_user.custom['favicon'] = current_app.config['UPLOAD_PATH_FOR_DB'] + '/' + fileName
            current_user.save()
            flash(u"网站图标修改成功！")
        except:
            flash(u"图片上传失败！")
    else:
        flash(u"请上传png/jpg/gif图片！")
    return redirect(url_for('admin.webSetting'))

@bpAdmin.route("/setCopyright", methods=['POST'])
@login_required
def setCopyright():
    copyright = request.form['copyright'].strip()
    if not strLength(copyright,1,100):
        flash(u"copyright最多100个字符")
        return redirect(url_for('admin.webSetting'))

    current_user.custom['copyright'] = copyright
    current_user.save()
    flash(u"copyright信息修改成功！")
    return redirect(url_for('admin.webSetting'))

@bpAdmin.route("/setStatisticalCode", methods=['POST'])
@login_required
def setStatisticalCode():
    statisticalCode = request.form['statisticalCode'].strip()
    if not strLength(statisticalCode,0,1000):
        flash(u"统计代码最多1000个字符")
        return redirect(url_for('admin.webSetting'))

    current_user.custom['statisticalCode'] = statisticalCode
    current_user.save()
    flash(u"统计代码修改成功！")
    return redirect(url_for('admin.webSetting'))

@bpAdmin.route("/setCommentCode", methods=['POST'])
@login_required
def setCommentCode():
    commentCode = request.form['commentCode'].strip()
    if not strLength(commentCode,0,2000):
        flash(u"评论代码最多2000个字符")
        return redirect(url_for('admin.webSetting'))

    current_user.custom['commentCode'] = commentCode
    current_user.save()
    flash(u"评论代码修改成功！")
    return redirect(url_for('admin.webSetting'))

@bpAdmin.route("/webTemplate")
@bpAdmin.route("/webTemplate/<tpl>")
@login_required
def webTemplate(tpl=None):
    themePath = os.path.join(current_app.config['BASE_DIR'], current_app.config['TPMPLATE_PATH'])
    themes = os.listdir(themePath)

    tpls = []
    for h in themes:
        tpls.append([h, '/%s/%s/%s' % (current_app.config['TPMPLATE_PATH'],h,'cover.jpg')])

    if not tpl:
        return render_template('admin/webTemplate.html',tpls=tpls)
    elif tpl in themes:
        current_user.custom['homeTemplate'] = 'theme/%s' % tpl
        current_user.save()
        flash(u'主题设置成功')
        return redirect(url_for('admin.webTemplate'))


