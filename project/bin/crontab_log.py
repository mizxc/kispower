# -*- coding: utf-8 -*-
#定时管理日志，如果日志文件大小超过50M清除日志内容


import os
from project.config import BaseConfig
from project.common.dataPreprocess import getStrTime
from project.common.filePreprocess import writeLog

if __name__ == '__main__':
    strTime = getStrTime()
    try:
        logs = os.listdir(BaseConfig.LOGS_PATH)
        for log in logs:
            path = os.path.join(BaseConfig.LOGS_PATH, log)
            #过滤掉crontab_,nginx.pid
            if 'crontab_' in log:continue
            if 'nginx.pid' == log:continue

            if 'mongodb' in log:
                if log != 'mongodb.log':
                    #删除因为重启而多生成的mongodb.log.....文件
                    os.remove(path)
                    continue
            #判断文件大小，如果超过50M，就重写文件为空
            size = os.path.getsize(path)
            if(size / 1000000) > 50.0:
                with open(path, 'w') as wf:
                    wf.write('%s | Logging greater than 50m, reset to empty\n' % strTime)
                writeLog(os.path.join(BaseConfig.LOGS_PATH, 'crontab_log.log'), strTime + ' | "%s":Logging greater than 50m, reset to empty'%log)

        info = strTime + ' | Log management: success'
    except Exception as e:
        info = strTime + ' | Log management: failed (%s)' % e

writeLog(os.path.join(BaseConfig.LOGS_PATH, 'crontab_log.log'), info)

