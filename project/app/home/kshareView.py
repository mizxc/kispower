# -*- coding: utf-8 -*-
# @Time    : 2019-12-21
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

from flask import current_app, request, flash, render_template, redirect, url_for,jsonify
from flask_login import current_user
from . import bpHome
from project.common.dataPreprocess import getPagingParameters
from project.model.km import KShare

@bpHome.route("/kshare")
@bpHome.route("/kshare/<page>")
def kshare(page=0):
    page = int(page)
    sk = getPagingParameters(page,12)
    ks = KShare.objects().order_by('-id')[sk[0]:sk[1]]
    return render_template('%s/kshare.html' % current_user.getCustom()['homeTemplate'],
                           ks=ks, page=page, mark='kshare')

@bpHome.route("/kispowerKShareShow/<id>")
def kispowerKShareShow(id):
    k = KShare.objects(id=id).first()
    k.pv += 1
    k.save()
    return render_template('admin/kispowerKShareShow.html',k=k,id=id)

@bpHome.route("/kispowerGetKShareData/<id>")
def kispowerGetKShareData(id):
    k = KShare.objects(id=id).first()
    mind = k.k
    # 判断显示模式，如果为两边显示，修改，root下的第一级方向
    if mind['meta']['displayMode'] == 'full':
        childrenLength = len(mind['data']['children'])
        halfLength = childrenLength / 2
        if 'children' in mind['data']:
            for index, c in enumerate(mind['data']['children']):
                if (index + 1) <= halfLength:
                    c['direction'] = 'right'
                else:
                    c['direction'] = 'left'
    else:
        if 'children' in mind['data']:
            for c in mind['data']['children']:
                c['direction'] = 'right'
    return jsonify({'status': True, 'data': mind})

@bpHome.route("/kispowerKShareShowTagTree/<id>")
def kispowerKShareShowTagTree(id):
    k = KShare.objects(id=id).first()
    return render_template('admin/kispowerKShareShowTagTree.html',k=k,id=id)

@bpHome.route("/kispowerKShareShowTagTreeGetData/<id>")
def kispowerKShareShowTagTreeGetData(id):
    k = KShare.objects(id=id).first()
    return jsonify({'status': True, 'data': k.k})


