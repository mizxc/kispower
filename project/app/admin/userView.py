# -*- coding: utf-8 -*-
# @Time    : 2019-12-20
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

import os
from flask import current_app, request, flash, render_template, redirect, url_for, jsonify
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import bpAdmin
from project.common.regular import reEmail
from project.model.user import User
from project.common.filePreprocess import allowedImage, creatFileName, allowedFileSize, removeFile

@bpAdmin.route("/userinfo")
@login_required
def userInfo():
    return render_template('admin/userInfo.html')

@bpAdmin.route("/setuserinfo", methods=['POST'])
@login_required
def setUserInfo():
    userName = request.form['userName']
    email = request.form['email']

    if len(userName) < 2 or len(userName) > 20:
        flash(u"请输入2-20个字符的用户名！")
        return redirect(url_for('admin.userInfo'))
    if not reEmail(email):
        flash(u"邮箱【%s】格式不对，请重新输入！" % email)
        return redirect(url_for('admin.userInfo'))
    if current_user.userName != userName:
        if User.objects(userName=userName).first():
            flash(u"用户名【%s】已经存在，请重新输入！" % userName)
            return redirect(url_for('admin.userInfo'))

    current_user.userName = userName
    current_user.email = email
    current_user.save()
    flash(u"信息修改成功！")
    return redirect(url_for('admin.userInfo'))

@bpAdmin.route("/setusericon", methods=['POST'])
@login_required
def setUserIcon():
    img = request.files.get('img')
    if not allowedFileSize(len(img.read()),1):
        flash(u"请上传小于1M的图片！")
        return redirect(url_for('admin.userInfo'))
    #文件read后，要重样把指针定位到开头
    img.seek(0)
    if img and allowedImage(img.filename):
        try:
            fileName = creatFileName(current_user.id, img.filename)
            img.save(os.path.join(current_app.config['UPLOAD_PATH'], fileName))
            if 'local/images/' not in current_user.icon:
                #删除以前的图片
                removeFile(os.path.join(current_app.config['STATIC_PATH'], current_user.icon))
            current_user.icon = current_app.config['UPLOAD_PATH_FOR_DB'] + '/' + fileName
            current_user.save()
            flash(u"头像修改成功！")
        except:
            flash(u"图片上传失败！")
    else:
        flash(u"请上传png/jpg/gif图片！")
    return redirect(url_for('admin.userInfo'))

@bpAdmin.route("/setuserpassword", methods=['POST'])
@login_required
def setUserPassword():
    oldPassword = request.form['oldPassword']
    newPassword = request.form['newPassword']

    if check_password_hash(current_user.password, oldPassword):
        if len(newPassword) >= 6 and len(newPassword) <= 18:
            current_user.password = generate_password_hash(newPassword)
            current_user.save()
            flash(u"密码修改成功！")
        else:
            flash(u"请输入6-18位新密码！")
    else:
        flash(u"原密码输入错误！")
    return redirect(url_for('admin.userInfo'))

@bpAdmin.route("/setuseraboutme", methods=['POST'])
@login_required
def setUserAboutMe():
    aboutMe = request.form['aboutMe']
    if len(aboutMe) > 15000:
        return jsonify({'status': False, 'info': u'请输入15000个字符内的about me'})
    current_user.aboutMe = aboutMe
    current_user.save()
    return jsonify({'status': True, 'info': u'aboutMe修改成功'})

@bpAdmin.route("/setUserSocial", methods=['POST'])
@login_required
def setUserSocial():
    img = request.files.get('img')
    weibo = request.form['weibo']
    if not allowedFileSize(len(img.read()),1):
        flash(u"请上传小于1M的图片！")
        return redirect(url_for('admin.userInfo'))
    #文件read后，要重样把指针定位到开头
    img.seek(0)
    if img and allowedImage(img.filename):
        try:
            fileName = creatFileName(current_user.id, img.filename)
            img.save(os.path.join(current_app.config['UPLOAD_PATH'], fileName))
            if 'local/images/' not in current_user.custom['weixin']:
                #删除以前的图片
                removeFile(os.path.join(current_app.config['STATIC_PATH'], current_user.custom['weixin']))
            current_user.custom['weixin'] = current_app.config['UPLOAD_PATH_FOR_DB'] + '/' + fileName
            flash(u"微信二维码修改成功！")
        except:
            flash(u"图片上传失败！")
    flash(u"微博链接修改成功！")
    current_user.custom['weibo'] = weibo
    current_user.save()
    return redirect(url_for('admin.userInfo'))