# -*- coding: utf-8 -*-
# @Time    : 2019-12-27
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

from flask import current_app, request, flash, render_template, redirect, url_for, jsonify
from flask_login import login_required, current_user
from . import bpAdmin
from project.common.dataPreprocess import strLength
from project.model.blog import *
from project.common.dataPreprocess import getStrTime,getLeadAndCover,getTagsFormStrTag

@bpAdmin.route("/blogColumn")
@login_required
def blogColumn():
    cs = Column.objects.order_by('+number')
    return render_template('admin/blogColumn.html', cs=cs)

@bpAdmin.route("/blogColumnAdd", methods=['POST'])
@login_required
def blogColumnAdd():
    title = request.form['title']
    introduction = request.form['introduction']

    if not strLength(title,1,30):
        flash(u'请输入60个字符内的专栏名称！')
        return redirect(url_for('admin.blogColumn'))
    if introduction and not strLength(introduction,1,100):
        flash(u'请输入100个字符内的专栏介绍！')
        return redirect(url_for('admin.blogColumn'))

    c = Column()
    c.title = title
    c.number = Column.objects.count()+1
    if introduction:c.introduction=introduction
    c.save()
    flash(u'专栏添加成功！')
    return redirect(url_for('admin.blogColumn'))

@bpAdmin.route("/blogColumnEdit/<id>", methods=['GET','POST'])
@login_required
def blogColumnEdit(id):
    c = Column.objects(id=id).first()
    if request.method == 'GET':
        return render_template('admin/blogColumnEdit.html', c=c)
    if request.method == 'POST':
        title = request.form['title']
        introduction = request.form['introduction']

        if not strLength(title, 1, 30):
            flash(u'请输入60个字符内的专栏名称！')
            return redirect(url_for('admin.blogColumnEdit',id=id))
        if introduction and not strLength(introduction, 1, 100):
            flash(u'请输入100个字符内的专栏介绍！')
            return redirect(url_for('admin.blogColumn',id=id))

        c.title = title
        c.introduction = introduction
        c.save()
        flash(u'专栏修改成功！')
        return redirect(url_for('admin.blogColumn'))

@bpAdmin.route("/blogColumnNumberChange/<number>/<direction>", methods=['GET'])
@login_required
def blogColumnNumberChange(number, direction):
    current = Column.objects(number=int(number)).first()
    currentNumber = int(number)
    if direction == 'up':
        next = Column.objects(number=int(number)-1).first()
    if direction == 'down':
        next = Column.objects(number=int(number)+1).first()
    nextNumber = next.number

    current.number = nextNumber
    current.save()
    next.number = currentNumber
    next.save()
    return redirect(url_for('admin.blogColumn'))

@bpAdmin.route("/blogColumnDelete/<id>", methods=['GET'])
@login_required
def blogColumnDelete(id):
    c = Column.objects(id=id).first()
    #先判断该专栏下是否有文章，有就不能删除
    if len(Post.objects(column=c))>0:
        flash(u'该专栏下有文章不能删除！')
        return redirect(url_for('admin.blogColumn'))
    #删除后，剩下的重新排编号
    c.delete()
    cs = Column.objects.order_by('+number')
    for index, c in enumerate(cs):
        c.number = index+1
        c.save()
    flash(u'专栏删除成功！')
    return redirect(url_for('admin.blogColumn'))

@bpAdmin.route("/blogColumnManage/<id>")
@login_required
def blogColumnManage(id):
    c = Column.objects(id=id).first()
    ps = Post.objects(column=c).order_by('-isTop','-id')
    return render_template('admin/blogColumnManage.html',c=c,ps=ps)

@bpAdmin.route("/blogPostAdd/<id>", methods=['GET','POST'])
@login_required
def blogPostAdd(id):
    c = Column.objects(id=id).first()
    if request.method == 'GET':
        return render_template('admin/blogPostAdd.html',c=c)
    if request.method == 'POST':
        title = request.form['title'].strip()
        tags = request.form['tags'].strip()
        video = request.form['video'].strip()
        content = request.form['content']

        if not strLength(title,1,100):
            return jsonify({'status': False, 'info': u'请输入100个字符内的标题'})
        if not strLength(tags,1,60):
            return jsonify({'status': False, 'info': u'请至少输入1个标签，60个字符内'})
        if not strLength(video,0,500):
            return jsonify({'status': False, 'info': u'请至少500个字符内视频嵌入代码'})
        if not strLength(content,1,50000):
            return jsonify({'status': False, 'info': u'请输入50000个字符内的内容'})

        p = Post()
        p.title = title
        p.tags = getTagsFormStrTag(tags)
        p.tagSource = tags
        p.video = video
        p.content = content
        temp = getLeadAndCover(content)
        p.lead = temp[0]
        p.cover = temp[1]
        p.writeTime = getStrTime()
        p.column = c
        p.save()
        c.postCount += 1
        c.save()
        return jsonify({'status': True, 'info': u'文章添加成功'})

@bpAdmin.route("/blogPostEdit/<id>", methods=['GET','POST'])
@login_required
def blogPostEdit(id):
    p = Post.objects(id=id).first()
    if request.method == 'GET':
        cs = Column.objects
        return render_template('admin/blogPostEdit.html',p=p,cs=cs)
    if request.method == 'POST':
        title = request.form['title'].strip()
        column = request.form['column']
        tags = request.form['tags'].strip()
        video = request.form['video'].strip()
        content = request.form['content']

        if not strLength(title, 1, 100):
            return jsonify({'status': False, 'info': u'请输入100个字符内的标题'})
        if not strLength(tags, 1, 60):
            return jsonify({'status': False, 'info': u'请至少输入1个标签，60个字符内'})
        if not strLength(video,0,500):
            return jsonify({'status': False, 'info': u'请至少500个字符内视频嵌入代码'})
        if not strLength(content, 1, 50000):
            return jsonify({'status': False, 'info': u'请输入50000个字符内的内容'})

        p.title = title
        p.tags = getTagsFormStrTag(tags)
        p.tagSource = tags
        p.video = video
        p.content = content
        temp = getLeadAndCover(content)
        p.lead = temp[0]
        p.cover = temp[1]
        if p.column.title != column:
            c = Column.objects(title=column).first()
            c.postCount += 1
            c.save()
            p.column.postCount -= 1
            p.column.save()
            p.column = c
        p.save()
        return jsonify({'status': True, 'info': u'文章修改成功'})

@bpAdmin.route("/blogPostDelete/<id>", methods=['GET'])
@login_required
def blogPostDelete(id):
    p = Post.objects(id=id).first()
    columnId = p.column.id
    p.column.postCount -= 1
    p.column.save()
    p.delete()
    return redirect(url_for('admin.blogColumnManage', id=columnId))

@bpAdmin.route("/blogPostIsTop/<id>/<isTop>", methods=['GET'])
@login_required
def blogPostIsTop(id,isTop):
    p = Post.objects(id=id).first()
    columnId = p.column.id
    if isTop == 'y':
        p.isTop = True
    elif isTop == 'n':
        p.isTop = False
    p.save()
    return redirect(url_for('admin.blogColumnManage', id=columnId))



