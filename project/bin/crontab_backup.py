# -*- coding: utf-8 -*-


import os
import zipfile
import shutil
from project.config import BaseConfig
from project.common.dataPreprocess import getStrTime
from project.common.filePreprocess import writeLog

def zipDir(dirpath,outFullName):
    """
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    zip = zipfile.ZipFile(outFullName,"w",zipfile.ZIP_DEFLATED)
    for path,dirnames,filenames in os.walk(dirpath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirpath,'')

        for filename in filenames:
            zip.write(os.path.join(path,filename),os.path.join(fpath,filename))
    zip.close()

def clearBackupFiles():
    #清除过期备份文件，只备份3天
    bs = 3*2
    files = os.listdir(BaseConfig.BACKUP_PATH)
    files.sort()
    count = len(files)
    if count>bs:
        for i in range(count-bs):
            path = os.path.join(BaseConfig.BACKUP_PATH, files[0])
            del files[0]
            if os.path.exists(path): os.remove(path)


if __name__ == '__main__':
    info = getStrTime()
    try:
        #备份用户上传的图片文件夹
        strTime = getStrTime().split(' ')[0]
        fileName = strTime + '_upload.zip'
        zipDir(BaseConfig.UPLOAD_PATH, os.path.join(BaseConfig.BACKUP_PATH,fileName))
        info += ' | "_upload" backup success'

        #备份mongodb数据库，导出后，zip压缩，再删除导出的文件夹
        mongodump = "/opt/kispower/mongodb/bin/mongodump"
        db = 'kispower'
        exportPath = os.path.join(BaseConfig.BACKUP_PATH,strTime+'_kispower.db')
        order = "%s -h 127.0.0.1:27017 -d %s -o %s" % (mongodump,db,exportPath)
        os.system(order)
        zipDir(exportPath, os.path.join(BaseConfig.BACKUP_PATH, strTime+'_kispower.db.zip'))
        if os.path.exists(exportPath):shutil.rmtree(exportPath)
        info += ' | "mongodb" backup success'

        #清除备份过期文件
        clearBackupFiles()
        info += ' | "clearBackupFiles" success'
    except Exception as e:
        info += ' | backup: failed (%s)' % e

    writeLog(os.path.join(BaseConfig.LOGS_PATH, 'crontab_backup.log'), info)
