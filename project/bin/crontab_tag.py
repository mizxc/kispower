# -*- coding: utf-8 -*-
#Statistics article labels: executed at 24 PM per night
import os
from mongoengine import connect

from project.model.blog import Post
from project.model.user import User
from project.config import BaseConfig
from project.common.dataPreprocess import getStrTime
from project.common.filePreprocess import writeLog


info = getStrTime()
try:
    connect(BaseConfig.DBNAME, host=BaseConfig.DBHOST, port=BaseConfig.DBPORT)
    ps = Post.objects
    tags = {}
    for p in ps:
        for t in p.tags:
            if t in tags:
                tags[t] += 1
            else:
                tags[t] = 1
    user = User.objects.first()
    if user:
        user.custom['tags'] = tags
        user.save()
        info += ' | Article tag statistics: success'
    else:
        info += ' | Article label statistics: the system does not exist users'

except Exception as e:
    info += ' | Article tag statistics: failed (%s)' % e

writeLog(os.path.join(BaseConfig.LOGS_PATH,'crontab_blogTag.log'),info)



