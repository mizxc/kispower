# -*- coding: utf-8 -*-
# @Time    : 2019-12-20
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

import os
from flask import current_app, render_template, redirect, url_for, send_from_directory
from flask_login import login_required
from . import bpAdmin

@bpAdmin.route("/")
@login_required
def adminIndex():
    return redirect(url_for('admin.timeManagementTodayBoard'))

#单一功能VIEW________________________________________________________________________
@bpAdmin.route("/feedbackAdd")
@login_required
def feedbackAdd():
    url = current_app.config['URL_FEEDBACK']
    return render_template('admin/feedbackAdd.html',url=url)

@bpAdmin.route("/guideAndVersionAndBackup")
@login_required
def guideAndVersionAndBackup():
    guide = current_app.config['URL_USERGUIDE']
    version = current_app.config['VERSION']
    versionUrl = current_app.config['URL_VERSION']
    backupFiles = os.listdir(current_app.config['BACKUP_PATH'])
    backupFiles.sort()
    return render_template('admin/guideAndVersionAndBackup.html',
                           guide=guide,
                           version=version,versionUrl=versionUrl,
                           backupFiles=backupFiles)

@bpAdmin.route("/backupFileDownload/<fileName>")
@login_required
def backupFileDownload(fileName):
    fileName += '.zip'
    return send_from_directory(current_app.config['BACKUP_PATH'], filename=fileName, as_attachment=True)
#单一功能VIEW________________________________________________________________________




