# -*- coding: utf-8 -*-
# @Time    : 2020-01-20
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

import os
from flask import current_app, request, flash, render_template, redirect, url_for, jsonify
from flask_login import login_required, current_user
from . import bpAdmin
from project.common.filePreprocess import allowedImage, creatFileName, allowedFileSize, removeFile

@bpAdmin.route("/slideSetting")
@login_required
def slideSetting():
    if request.method == 'GET':
        return render_template('admin/slideSetting.html')

@bpAdmin.route("/uploadSlide/<index>", methods=['POST'])
@login_required
def uploadSlide(index):
    index = int(index)
    mainTitle = request.form['mainTitle']
    subTitle = request.form['subTitle']
    link = request.form['link']
    img = request.files.get('img')
    if not allowedFileSize(len(img.read()),1):
        flash(u"请上传小于1M的图片！")
        return redirect(url_for('admin.slideSetting'))
    #文件read后，要重样把指针定位到开头
    img.seek(0)
    if img and allowedImage(img.filename):
        try:
            fileName = creatFileName(current_user.id, img.filename)
            img.save(os.path.join(current_app.config['UPLOAD_PATH'], fileName))
            if current_user.custom['slide'][index][0] and ('local/images/' not in current_user.custom['slide'][index][0]):
                #删除以前的图片
                removeFile(os.path.join(current_app.config['STATIC_PATH'], current_user.custom['slide'][index][0]))
            current_user.custom['slide'][index][0] = current_app.config['UPLOAD_PATH_FOR_DB'] + '/' + fileName
            current_user.custom['slide'][index][1] = mainTitle
            current_user.custom['slide'][index][2] = subTitle
            current_user.custom['slide'][index][3] = link
            current_user.save()
            flash(u"幻灯片修改成功！")
        except:
            flash(u"图片上传失败！")
    else:
        current_user.custom['slide'][index][1] = mainTitle
        current_user.custom['slide'][index][2] = subTitle
        current_user.custom['slide'][index][3] = link
        current_user.save()
    return redirect(url_for('admin.slideSetting'))

@bpAdmin.route("/deleteSlide/<index>")
@login_required
def deleteSlide(index):
    index = int(index)
    if 'local/images/' not in current_user.custom['slide'][index][0]:
        # 删除以前的图片
        removeFile(os.path.join(current_app.config['STATIC_PATH'], current_user.custom['slide'][index][0]))
    current_user.custom['slide'][index][0] = None
    current_user.custom['slide'][index][1] = None
    current_user.custom['slide'][index][2] = None
    current_user.custom['slide'][index][3] = None
    current_user.save()
    flash(u"幻灯片删除成功！")
    return redirect(url_for('admin.slideSetting'))
