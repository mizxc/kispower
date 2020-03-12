# -*- coding: utf-8 -*-
# @Time    : 2019-12-29
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

import json
import uuid
from flask import current_app, request, flash, render_template, redirect, url_for, jsonify
from flask_login import login_required, current_user
from . import bpAdmin
from project.common.dataPreprocess import strLength,getTagsFormStrTag
from project.model.km import *

@bpAdmin.route("/kispowerKClass")
@login_required
def kispowerKClass():
    kcs = KClass.objects.order_by('-isTop','-id')
    return render_template('admin/kispowerKClass.html',kcs=kcs)

@bpAdmin.route("/kispowerKClassAdd", methods=['POST'])
@login_required
def kispowerKClassAdd():
    title = request.form['title']
    introduction = request.form['introduction']

    if not strLength(title,1,60):
        flash(u'请输入60个字符内的名称！')
        return redirect(url_for('admin.kispowerKClass'))
    if introduction and not strLength(introduction,1,1000):
        flash(u'请输入1000个字符内的介绍！')
        return redirect(url_for('admin.kispowerKClass'))

    k = KClass()
    k.title = title
    if introduction:k.introduction=introduction
    k.k = creatNewKClass(title,current_user.userName)
    k.save()
    flash(u'根目录添加成功！')
    return redirect(url_for('admin.kispowerKClass'))

@bpAdmin.route("/kispowerKClassEdit/<id>", methods=['GET','POST'])
@login_required
def kispowerKClassEdit(id):
    k = KClass.objects(id=id).first()
    if request.method == 'GET':
        return render_template('admin/kispowerKClassEdit.html',k=k)
    if request.method == 'POST':
        title = request.form['title']
        introduction = request.form['introduction']

        if not strLength(title, 1, 60):
            flash(u'请输入60个字符内的名称！')
            return redirect(url_for('admin.kispowerKClassEdit',id=id))
        if introduction and not strLength(introduction, 1, 1000):
            flash(u'请输入1000个字符内的介绍！')
            return redirect(url_for('admin.kispowerKClassEdit',id=id))

        k.title = title
        k.introduction = introduction
        k.save()
        flash(u'根目录修改成功！')
        return redirect(url_for('admin.kispowerKClass'))

@bpAdmin.route("/kispowerKClassDelete/<id>", methods=['GET'])
@login_required
def kispowerKClassDelete(id):
    k = KClass.objects(id=id).first()
    #页面上删除所有子节点后，根节点数据字典就不包含key:childpren
    if 'children' in k.k['data']:
        if len(k.k['data']['children'])!=0:
            flash('该根目录下有子节点，不能删除，请删除完子节点后，再来删除')
        else:
            k.delete()
    else:
        k.delete()
    return redirect(url_for('admin.kispowerKClass'))

@bpAdmin.route("/kispowerKClassIsTop/<id>", methods=['GET'])
@login_required
def kispowerKClassIsTop(id):
    k = KClass.objects(id=id).first()
    if k.isTop == True:k.isTop=False
    else:k.isTop=True
    k.save()
    flash(u'置顶状态修改成功')
    return redirect(url_for('admin.kispowerKClass'))

@bpAdmin.route("/kispowerKClassShow/<id>")
@login_required
def kispowerKClassShow(id):
    return render_template('admin/kispowerKClassShow.html',id=id)

@bpAdmin.route("/kispowerGetMindData/<id>")
@login_required
def kispowerGetMindData(id):
    k = KClass.objects(id=id).first()
    mind = k.k
    #判断显示模式，如果为两边显示，修改，root下的第一级方向
    if mind['meta']['displayMode'] == 'full':
        if 'children' in mind['data']:
            childrenLength = len(mind['data']['children'])
            halfLength = childrenLength/2
            for index, c in enumerate(mind['data']['children']):
                if (index+1)<=halfLength:
                    c['direction'] = 'right'
                else:
                    c['direction'] = 'left'
    else:
        if 'children' in mind['data']:
            for c in mind['data']['children']:
                c['direction'] = 'right'
    return jsonify({'status': True, 'data': mind})

@bpAdmin.route("/kispowerPostMindData/<id>",methods=['POST'])
@login_required
def kispowerPostMindData(id):
    k = KClass.objects(id=id).first()
    action = request.form['action']
    mind = json.loads(request.form['data'])

    if action == 'reload':
        k.k['meta']['saveTime'] = getStrTime()
        k.k = mind
        k.save()
        return jsonify({'status': True,})
    elif action == 'save':
        k.k['meta']['saveTime'] = getStrTime()
        if mind['data'] != k.k['data']:
            k.k['meta']['version'] = round(k.k['meta']['version'] +0.1,1)
            k.k['data'] = mind['data']
        k.save()
        return jsonify({'status': True,'data':'v%s / %s'%(k.k['meta']['version'],k.k['meta']['saveTime'])})

    elif action == 'import':
        allData = mind['allData']
        currentNodeId = mind['currentNodeId']
        importNode = mind['importNode']

        #递归修改导入节点的ID值
        def recursion1(data):
            data['id'] = str(uuid.uuid1())
            if 'children' in data:
                for i in data['children']:
                    recursion1(i)
        recursion1(importNode)

        #递归修改导入目标节点的值
        def recursion2(data):
            if data['id'] == currentNodeId:
                if 'children' in data:
                    data['children'].append(importNode)
                    return
                else:
                    data['children'] = [importNode]
            else:
                if 'children' in data:
                    for i in data['children']:
                        recursion2(i)

        recursion2(allData['data'])
        allData['meta']['version'] = round(k.k['meta']['version'] + 0.1, 1)
        allData['meta']['saveTime'] = getStrTime()
        k.k = allData
        k.save()
        return jsonify({'status': True,'msg': u'数据导入成功'})

@bpAdmin.route("/kispowerPostShareData/<id>",methods=['POST'])
@login_required
def kispowerPostShareData(id):
    shareTitle = request.form['shareTitle']
    shareTag = request.form['shareTag']
    shareMode = request.form['shareMode']
    shareIntroduction = request.form['shareIntroduction']
    #检查字段
    if not strLength(shareTitle,1,60):
        return jsonify({'status': False, 'msg': u'请输入60个字符内标题'})
    if not strLength(shareTag,1,30):
        return jsonify({'status': False, 'msg': u'请输入30个字符内标签'})
    if not strLength(shareIntroduction,1,10000):
        return jsonify({'status': False, 'msg': u'请输入10000个字符内简介'})
    shareData = json.loads(request.form['shareData'])
    #必须设置root节点
    source = id+shareData['data']['id']
    shareData['data']['id'] = 'root'
    #设置节点显示模式
    shareData['meta']['displayMode'] = shareMode
    if 'children' in shareData['data'] and len(shareData['data']['children'])>0:
        ks = KShare.objects(source=source).first()
        if ks:
            ks.title = shareTitle
            ks.tag = getTagsFormStrTag(shareTag)
            ks.introduction = shareIntroduction
            ks.introductionHtml = shareIntroduction.replace('\n', '<br>')
            ks.shareTime = getStrTime()
            ks.k = shareData
            ks.save()
            #同步到分享库
            try:
                ks.postKShareToBase(shareTag,current_user.userName,current_app.config['WEBSITE'],current_app.config['URL_KSHARE_POST'])
            except:
                pass
            return jsonify({'status': True, 'msg': u'该节点已经分享过，已为你更新为该节点的最新版本'})
        else:
            share = KShare()
            share.title = shareTitle
            share.tag = getTagsFormStrTag(shareTag)
            share.introduction = shareIntroduction
            share.introductionHtml = shareIntroduction.replace('\n','<br>')
            share.shareTime = getStrTime()
            share.k = shareData
            share.source = source
            share.save()
            #分享到分享库
            try:
                share.postKShareToBase(shareTag,current_user.userName,current_app.config['WEBSITE'],current_app.config['URL_KSHARE_POST'])
            except:
                pass
            return jsonify({'status': True, 'msg':u'分享成功！请去管理界面右边菜单栏（知识管理-我的知识分享）查看'})
    else:
        return jsonify({'status': False, 'msg': u'该节点没有子节点，不能分享'})

@bpAdmin.route("/kispowerGetIsSharedNode",methods=['POST'])
@login_required
def kispowerGetIsSharedNode():
    kClassId = request.form['kClassId']
    nodeId = request.form['nodeId']

    #组装source
    source = kClassId+nodeId
    ks = KShare.objects(source=source).first()
    if ks:
        data = {
            'title':ks.title,
            'tag':' '.join(ks.tag),
            'mode':ks.k['meta']['displayMode'],
            'introduction':ks.introduction
        }
        return jsonify({'status': True, 'data': data})
    else:
        return jsonify({'status': False})

@bpAdmin.route("/kispowerKShare")
@login_required
def kispowerKShare():
    ks = KShare.objects.order_by('-shareTime')
    return render_template('admin/kispowerKShare.html',ks=ks)

@bpAdmin.route("/kispowerKShareDelete/<id>",methods=['POST'])
@login_required
def kispowerKShareDelete(id):
    k = KShare.objects(id=id).first()
    # 提交删除到分享库
    try:
        k.deleteKShareFromBase(current_app.config['WEBSITE'],current_app.config['URL_KSHARE_DELETE'])
    except:
        pass
    k.delete()
    return jsonify({'status':True,'info':u'删除成功！'})



