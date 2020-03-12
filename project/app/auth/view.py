# -*- coding: utf-8 -*-
# @Time    : 2019-12-21
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, request, flash, render_template, redirect, url_for, session
from flask_login import login_user, logout_user, login_required, current_user
from . import bpAuth
from project.model.user import User
from project.common.regular import reEmail

@bpAuth.route("/register", methods=['GET', 'POST'])
def userRegister():
    """
    第一个用户注册默认为管理员，拥有所有权限
    以后注册的用户为partner，拥有某分支的知识管理权限
    """
    if current_user.is_authenticated:
        return redirect(url_for('admin.adminIndex'))
    if request.method == 'GET':
        return render_template('admin/register.html')
    if request.method == 'POST':
        if User.objects.count() != 0:
            flash(u"你已经注册过了，请登陆！")
            return redirect(url_for('auth.userLogin'))

        userName = request.form['userName']
        email = request.form['email']
        password = request.form['password']

        if len(userName) < 2 or len(userName) > 20:
            flash(u"请输入2-20个字符的用户名！")
            return redirect(url_for('auth.userRegister'))
        if not reEmail(email):
            flash(u"邮箱【%s】格式不对，请重新输入！" % email)
            return redirect(url_for('auth.userRegister'))
        if User.objects(userName=userName).first():
            flash(u"用户名【%s】已经存在，请重新输入！" % userName)
            return redirect(url_for('auth.userRegister'))
        if len(password) < 6 or len(password) > 18:
            flash(u"请输入6-18位密码！")
            return redirect(url_for('auth.userRegister'))

        user = User()
        user.userName = userName
        user.email = email
        user.password = generate_password_hash(password)
        user.save()
        flash(u"注册成功，请登陆！")
        return redirect(url_for('auth.userLogin'))

@bpAuth.route("/login", methods=['GET', 'POST'])
def userLogin():
    # 判断是否登陆
    if current_user.is_authenticated:
        return redirect(url_for('admin.adminIndex'))
    if request.method == 'GET':
        return render_template('admin/login.html')
    if request.method == 'POST':
        userName = request.form['userName']
        password = request.form['password']
        user = User.objects(userName=userName).first()
        if not user:
            flash(u"用户【%s】不存在！" % userName)
            return redirect(url_for('auth.userLogin'))
        if check_password_hash(user.password, password):
            login_user(user)
            session.permanent = True
            return redirect(url_for('admin.adminIndex'))
        else:
            flash(u"密码输入错误！")
            return redirect(url_for('auth.userLogin'))

@bpAuth.route("/loginOut", methods=['GET', 'POST'])
@login_required
def userLoginOut():
    logout_user()
    flash('你已经退出登陆！')
    return redirect(url_for('auth.userLogin'))
