# -*- coding: utf-8 -*-
# @Time    : 2019-12-20
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

import os
from flask import current_app, request, flash, render_template, redirect, url_for
from flask_login import login_required, current_user
from . import bpHome
from project.model.photoAlbum import *
from project.common.dataPreprocess import getPagingParameters

@bpHome.route("/photoAlbum")
def photoAlbum():
    return render_template('%s/photoAlbum.html' % current_user.getCustom()['homeTemplate'],
                           mark='photo')

@bpHome.route("/photo/<albumId>")
@bpHome.route("/photo/<albumId>/<page>")
def photo(albumId,page=0):
    page = int(page)
    sk = getPagingParameters(page,21)
    a = Album.objects(id=albumId).first()
    if a.isShow:
        ps = Photo.objects(album=a).order_by('-isTop','-id')[sk[0]:sk[1]]
    else:
        ps = []
    return render_template('%s/photo.html' % current_user.getCustom()['homeTemplate'],
                           ps=ps,a=a,page=page,mark='photo')



