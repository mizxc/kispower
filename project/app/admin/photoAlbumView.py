# -*- coding: utf-8 -*-
# @Time    : 2019-12-27
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

import os
from flask import current_app, request, flash, render_template, redirect, url_for
from flask_login import login_required, current_user
from . import bpAdmin
from project.common.dataPreprocess import strLength
from project.model.photoAlbum import *
from project.common.filePreprocess import allowedImage, creatFileName, allowedFileSize, removeFile
from project.common.dataPreprocess import getPagingParameters

@bpAdmin.route("/photoAlbum")
@login_required
def photoAlbum():
    albums = Album.objects.order_by('+number')
    photos = Photo.objects.order_by('-id')[0:20]
    return render_template('admin/photoAlbum.html',albums=albums,photos=photos)

@bpAdmin.route("/photoAlbumAdd", methods=['POST'])
@login_required
def photoAlbumAdd():
    title = request.form['title']
    isShow = request.form['isShow']
    introduction = request.form['introduction']

    if not strLength(title,1,60):
        flash(u'请输入60个字符内的相册名称！')
        return redirect(url_for('admin.photoAlbum'))

    if isShow == 'y':
        isShow = True
    else:
        isShow = False

    if introduction and not strLength(introduction,1,1000):
        flash(u'请输入1000个字符内的栏目介绍！')
        return redirect(url_for('admin.photoAlbum'))

    p = Album()
    p.title = title
    p.isShow = isShow
    p.number = Album.objects.count()+1
    if introduction:p.introduction=introduction
    p.save()
    flash(u'相册创建成功！')
    return redirect(url_for('admin.photoAlbum'))

@bpAdmin.route("/photoAlbumEdit/<id>", methods=['GET','POST'])
@login_required
def photoAlbumEdit(id):
    p = Album.objects(id=id).first()
    if request.method == 'GET':
        return render_template('admin/photoAlbumEdit.html',p=p)
    if request.method == 'POST':
        title = request.form['title']
        isShow = request.form['isShow']
        introduction = request.form['introduction']

        if not strLength(title, 1, 60):
            flash(u'请输入60个字符内的相册名称！')
            return redirect(url_for('admin.photoAlbum'))

        if isShow == 'y':
            isShow = True
        else:
            isShow = False

        if introduction and not strLength(introduction, 1, 1000):
            flash(u'请输入1000个字符内的栏目介绍！')
            return redirect(url_for('admin.photoAlbum'))

        p.title = title
        p.isShow = isShow
        p.introduction = introduction
        p.save()
        flash(u'相册修改成功！')
        return redirect(url_for('admin.photoAlbum'))

@bpAdmin.route("/photoAlbumSort/<number>/<direction>", methods=['GET'])
@login_required
def photoAlbumSort(number, direction):
    current = Album.objects(number=int(number)).first()
    currentNumber = int(number)
    if direction == 'up':
        next = Album.objects(number=int(number)-1).first()
    if direction == 'down':
        next = Album.objects(number=int(number)+1).first()
    nextNumber = next.number

    current.number = nextNumber
    current.save()
    next.number = currentNumber
    next.save()
    return redirect(url_for('admin.photoAlbum'))

@bpAdmin.route("/photoAlbumDelete/<id>", methods=['GET'])
@login_required
def photoAlbumDelete(id):
    pa = Album.objects(id=id).first()
    #如果该相册有图片，不能删除
    ps = Photo.objects(album=pa)
    if len(ps)>0:
        flash(u'该相册下包含有图像，不能删除，请先删除图像后，再来删除相册！')
        return redirect(url_for('admin.photoAlbum'))
    pa.delete()
    #删除后，剩下的重新排编号
    ps = Album.objects.order_by('+number')
    for index, p in enumerate(ps):
        p.number = index+1
        p.save()
    flash(u'相册删除成功！')
    return redirect(url_for('admin.photoAlbum'))

@bpAdmin.route("/photoAlbumManage/<id>")
@login_required
def photoAlbumManage(id):
    pa = Album.objects(id=id).first()
    ps = Photo.objects(album=pa).order_by('-isTop','-id')
    return render_template('admin/photoAlbumManage.html',pa=pa,ps=ps)

@bpAdmin.route("/photoAlbumPhotoAdd", methods=['POST'])
@login_required
def photoAlbumPhotoAdd():
    albumId = request.form['albumId']
    if not albumId:
        flash(u'请先添加相册！')
        return redirect(url_for('admin.photoAlbum'))
    pa = Album.objects(id=albumId).first()
    introduction = request.form['introduction']

    if len(introduction)>1000:
        flash(u'请输入1000个字符内的图片描述！')
        return redirect(url_for('admin.photoAlbum'))

    p = Photo()
    p.introduction = introduction

    photo = request.files.get('photo')
    #其他字段判断完再判断图片上传
    photoPath = None
    if photo and allowedImage(photo.filename):
        if allowedFileSize(len(photo.read()), 2):
            photo.seek(0)
            p.title = photo.filename[:50]
            fileName = creatFileName(current_user.id, photo.filename)
            photo.save(os.path.join(current_app.config['UPLOAD_PHOTOALBUM_PATH'], fileName))
            photoPath = current_app.config['UPLOAD_PATH_PHOTOALBUM_FOR_DB'] + '/' + fileName
        else:
            flash(u"请上传小于2M的图片！")
            return redirect(url_for('admin.photoAlbum'))
    else:
        flash(u"请上传png/jpg/gif图片")
        return redirect(url_for('admin.photoAlbum'))
    p.path = photoPath

    p.album = pa
    p.save()

    pa.photoCount += 1
    pa.save()
    flash(u'图像添加成功！')
    return redirect(url_for('admin.photoAlbum'))

@bpAdmin.route("/photoAlbumPhotoDelete/<id>", methods=['GET'])
@login_required
def photoAlbumPhotoDelete(id):
    p = Photo.objects(id=id).first()
    albumId = p.album.id
    if p.path:
        removeFile(os.path.join(current_app.config['STATIC_PATH'], p.path))
    p.delete()
    flash(u'图像删除成功！')

    p.album.photoCount -= 1
    p.album.save()
    return redirect(url_for('admin.photoAlbumManage', id=albumId))

@bpAdmin.route("/photoAlbumPhotoIsTop/<albumId>/<photoId>/<isTop>", methods=['GET'])
@login_required
def photoAlbumPhotoIsTop(albumId,photoId,isTop):
    p = Photo.objects(id=photoId).first()
    if isTop == 'y':
        p.isTop = True
        flash(u'置顶成功！')
    elif isTop == 'n':
        p.isTop = False
        flash(u'取消置顶成功！')
    p.save()
    return redirect(url_for('admin.photoAlbumManage', id=albumId))



