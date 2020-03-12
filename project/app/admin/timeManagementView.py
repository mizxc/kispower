# -*- coding: utf-8 -*-
# @Time    : 2019-12-24
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

import datetime
from flask import current_app, request, flash, render_template, redirect, url_for, jsonify
from flask_login import login_required, current_user
from . import bpAdmin
from project.common.dataPreprocess import strLength, strToDatetime
from project.model.timeManagement import *
from project.common.dataPreprocess import getPagingParameters

@bpAdmin.route("/timeManagementTodayBoard")
@login_required
def timeManagementTodayBoard():
    currentDate = str(datetime.datetime.now()).split(' ')[0]
    dp = DailyPlan.objects(whichDay=currentDate).first()
    return render_template('admin/timeManagementTodayBoard.html',dp=dp)

@bpAdmin.route("/timeManagementBoard/<planType>/<id>")
@login_required
def timeManagementBoard(planType,id):
    if planType == 'yp':
        p = YearlyPlan.objects(id=id).first()
        sps = MonthlyPlan.objects(yearlyPlan=p).order_by('-id')
        subPlanType = 'mp'
    elif planType == 'mp':
        p = MonthlyPlan.objects(id=id).first()
        sps = WeeklyPlan.objects(monthlyPlan=p).order_by('-id')
        subPlanType = 'wp'
    elif planType == 'wp':
        p = WeeklyPlan.objects(id=id).first()
        sps = DailyPlan.objects(weeklyPlan=p).order_by('-id')
        subPlanType = 'dp'
    elif planType == 'dp':
        p = DailyPlan.objects(id=id).first()
        sps = []
        subPlanType = ''

    return render_template('admin/timeManagementBoard.html',
                           planType=planType,p=p,sps=sps,subPlanType=subPlanType)

@bpAdmin.route("/timeManagementWriteSummarize/<planType>/<id>",methods=['GET','POST'])
@login_required
def timeManagementWriteSummarize(planType,id):
    if planType == 'yp':
        p = YearlyPlan.objects(id=id).first()
    elif planType == 'mp':
        p = MonthlyPlan.objects(id=id).first()
    elif planType == 'wp':
        p = WeeklyPlan.objects(id=id).first()
    elif planType == 'dp':
        p = DailyPlan.objects(id=id).first()

    if request.method == 'GET':
        return render_template('admin/timeManagementWriteSummarize.html',
                               planType=planType,p=p)

    if request.method == 'POST':
        summarize = request.form['summarize']
        if len(summarize)>15000:
            return jsonify({'status': False, 'msg': u'请输入15000个字符内的总结！'})
        p.summarize = summarize
        p.save()
        url = url_for('admin.timeManagementBoard',planType=planType,id=id)
        return jsonify({'status': True, 'msg': u'总结提交成功！','url':url})

@bpAdmin.route("/timeManagementGetParentPlans",methods=['POST'])
@login_required
def timeManagementGetParentPlans():
    id = request.form['id']
    planType = request.form['planType']
    p = None
    if planType == 'yp':
        p = YearlyPlan.objects(id=id).first()
    elif planType == 'mp':
        p = MonthlyPlan.objects(id=id).first()
    elif planType == 'wp':
        p = WeeklyPlan.objects(id=id).first()
    html = ''
    if p:
        for item in p.plans:
            if item.isDone:
                done = '<i class="mdi mdi-check"></i>'
            else:
                done = ''
            if item.level == 'L1':
                html += '<li><label class="alert alert-danger">紧急重要：%s %s</label></li>' % (item.title,done)
            elif item.level == 'L2':
                html += '<li><label class="alert alert-warning">紧急不重要：%s %s</label></li>' % (item.title,done)
            elif item.level == 'L3':
                html += '<li><label class="alert alert-info">重要不紧急：%s %s</label></li>' % (item.title,done)
            elif item.level == 'L4':
                html += '<li><label class="alert alert-success">不重要不紧急：%s %s</label></li>' % (item.title,done)
        return jsonify({'status': True, 'data': {'parentPlanTitle':p.title,'parentPlanJobs':html}})
    else:
        return jsonify({'status': False})

@bpAdmin.route("/timeManagementPlanDone",methods=['POST'])
@login_required
def timeManagementPlanDone():
    try:
        id = request.form['id']
        planType = request.form['planType']
        number = int(request.form['number'])
        if planType == 'yp':
            p = YearlyPlan.objects(id=id).first()
            if p.plans[number].isDone == False:
                p.plans[number].isDone = True
            else:
                p.plans[number].isDone = False
            doneCount = 0
            for i in p.plans:
                if i.isDone:doneCount+=1
            p.doneCount = doneCount
            p.save()
        elif planType == 'mp':
            p = MonthlyPlan.objects(id=id).first()
            if p.plans[number].isDone == False:
                p.plans[number].isDone = True
            else:
                p.plans[number].isDone = False
            doneCount = 0
            for i in p.plans:
                if i.isDone: doneCount += 1
            p.doneCount = doneCount
            p.save()
        elif planType == 'wp':
            p = WeeklyPlan.objects(id=id).first()
            if p.plans[number].isDone == False:
                p.plans[number].isDone = True
            else:
                p.plans[number].isDone = False
            doneCount = 0
            for i in p.plans:
                if i.isDone: doneCount += 1
            p.doneCount = doneCount
            p.save()
        elif planType == 'dp':
            p = DailyPlan.objects(id=id).first()
            if p.plans[number].isDone == False:
                p.plans[number].isDone = True
            else:
                p.plans[number].isDone = False
            doneCount = 0
            for i in p.plans:
                if i.isDone: doneCount += 1
            p.doneCount = doneCount
            p.save()
        return jsonify({'status': True, 'info': u'提交任务成功！'})
    except:
        return jsonify({'status':False,'info':u'提交任务失败！'})

#年计划____________________________________________________________________________________________
@bpAdmin.route("/timeManagementYearlyPlan")
@login_required
def timeManagementYearlyPlan():
    levels = current_app.config['PLAN_LEVEL']
    yps = YearlyPlan.objects.order_by('-id')
    return render_template('admin/timeManagementYearlyPlan.html',
                           levels=levels,yps=yps)

@bpAdmin.route("/timeManagementYearlyPlanAdd",methods=['POST'])
@login_required
def timeManagementYearlyPlanAdd():
    title = request.form['title']
    startTime = request.form['startTime']
    endTime = request.form['endTime']

    planLevel = request.form.getlist('planLevel[]')
    planTitle = request.form.getlist('planTitle[]')

    if not strLength(title,1,100):
        return jsonify({'status': False, 'info': u'请输入1-100个字符的年计划标题'})
    if not startTime or not endTime:
        return jsonify({'status': False, 'info': u'请选择时间范围'})

    startTime = strToDatetime('%s 00:00:00' % startTime)
    endTime = strToDatetime('%s 23:59:59' % endTime)
    if endTime <= startTime:
        return jsonify({'status': False, 'info': u'结束时间必须要晚于开始时间'})

    #判断年计划时间是否冲突
    yps = YearlyPlan.objects
    for i in yps:
        if not (startTime>i.endTime or endTime<i.startTime):
            return jsonify({'status': False, 'info': u'年计划时间范围（%s - %s）与其他年计划时间（%s - %s）冲突！' %
                  (startTime,endTime,i.startTime,i.endTime)})

    plans = []
    for index, t in enumerate(planTitle):
        if len(t) > 0:
            p = Plan()
            p.title = t
            p.level = planLevel[index]
            plans.append(p)

    yearlyPlan = YearlyPlan()
    yearlyPlan.title = title
    yearlyPlan.startTime = startTime
    yearlyPlan.endTime = endTime
    yearlyPlan.plans = plans
    yearlyPlan.save()
    return jsonify({'status': True, 'info': u'年计划添加成功'})

@bpAdmin.route("/timeManagementYearlyPlanEdit/<id>",methods=['GET','POST'])
@login_required
def timeManagementYearlyPlanEdit(id):
    yearlyPlan = YearlyPlan.objects(id=id).first()
    levels = current_app.config['PLAN_LEVEL']
    if request.method == 'GET':
        return render_template('admin/timeManagementYearlyPlanEdit.html',
                               levels=levels, yearlyPlan=yearlyPlan,
                               startTime=str(yearlyPlan.startTime).split(' ')[0],
                               endTime=str(yearlyPlan.endTime).split(' ')[0])

    if request.method == 'POST':
        title = request.form['title']
        startTime = request.form['startTime']
        endTime = request.form['endTime']

        planLevel = request.form.getlist('planLevel[]')
        planTitle = request.form.getlist('planTitle[]')
        isDone = request.form.getlist('isDone[]')

        if not strLength(title,1,100):
            return jsonify({'status': False, 'info': u'请输入1-100个字符的年计划标题'})
        if not startTime or not endTime:
            return jsonify({'status': False, 'info': u'请选择时间范围'})

        startTime = strToDatetime('%s 00:00:00' % startTime)
        endTime = strToDatetime('%s 23:59:59' % endTime)
        if endTime <= startTime:
            return jsonify({'status': False, 'info': u'结束时间要晚于开始时间'})

        # 判断年计划时间是否冲突
        yps = YearlyPlan.objects
        for i in yps:
            if i == yearlyPlan: continue
            if not (startTime > i.endTime or endTime < i.startTime):
                return jsonify({'status': False, 'info': u'年计划时间范围（%s - %s）与其他年计划时间（%s - %s）冲突！' %
                                                         (startTime, endTime, i.startTime, i.endTime)})

        plans = []
        for index, t in enumerate(planTitle):
            if len(t)>0:
                p = Plan()
                p.title = t
                p.level = planLevel[index]
                if isDone[index] == 'y':
                    p.isDone = True
                else:
                    p.isDone = False
                plans.append(p)
        yearlyPlan.title = title
        yearlyPlan.startTime = startTime
        yearlyPlan.endTime = endTime
        yearlyPlan.plans = plans
        yearlyPlan.save()
        return jsonify({'status': True, 'info': u'年计划修改成功'})

@bpAdmin.route("/timeManagementYearlyPlanDelete/<id>",methods=['GET'])
@login_required
def timeManagementYearlyPlanDelete(id):
    #有子计划不能删除
    p = YearlyPlan.objects(id=id).first()
    if len(MonthlyPlan.objects(yearlyPlan=p))>0:
        flash(u'该年计划有下属月计划，不能删除，请先删除下属月计划后，再删除年计划')
    else:
        p.delete()
        flash(u'年计划删除成功')
    return redirect(url_for('admin.timeManagementYearlyPlan'))
#年计划____________________________________________________________________________________________

#月计划____________________________________________________________________________________________
@bpAdmin.route("/timeManagementMonthlyPlan")
@login_required
def timeManagementMonthlyPlan():
    levels = current_app.config['PLAN_LEVEL']
    mps = MonthlyPlan.objects.order_by('-id')
    yps = YearlyPlan.objects.order_by('-id')
    return render_template('admin/timeManagementMonthlyPlan.html',
                           levels=levels,mps=mps,yps=yps)

@bpAdmin.route("/timeManagementMonthlyPlanAdd",methods=['POST'])
@login_required
def timeManagementMonthlyPlanAdd():
    title = request.form['title']
    yearlyPlanId = request.form['yearlyPlanId']
    startTime = request.form['startTime']
    endTime = request.form['endTime']
    planLevel = request.form.getlist('planLevel[]')
    planTitle = request.form.getlist('planTitle[]')

    if not strLength(title,1,100):
        return jsonify({'status': False, 'info': u'请输入1-100个字符的月计划标题！'})
    if not startTime or not endTime:
        return jsonify({'status': False, 'info': u'请选择时间范围'})

    startTime = strToDatetime('%s 00:00:00' % startTime)
    endTime = strToDatetime('%s 23:59:59' % endTime)
    if endTime <= startTime:
        return jsonify({'status': False, 'info': u'结束时间必须要晚于开始时间'})

    y = YearlyPlan.objects(id=yearlyPlanId).first()
    #时间范围判断
    #月计划的时间范围必须在年计划的时间范围内
    if not (startTime>=y.startTime and endTime<=y.endTime):
        return jsonify({'status': False, 'info': u'月计划的时间范围必须在年计划的时间范围内'})
    #该年计划下的月计划时间范围不冲突
    mps = MonthlyPlan.objects(yearlyPlan=y)
    for i in mps:
        if not (startTime >= i.endTime or endTime <= i.startTime):
            return jsonify({'status': False, 'info': u'月计划的时间范围（%s - %s）和“%s”的时间范围（%s - %s）冲突' %
                  (startTime,endTime,i.title,i.startTime,i.endTime)})

    plans = []
    for index, t in enumerate(planTitle):
        if len(t) > 0:
            p = Plan()
            p.title = t
            p.level = planLevel[index]
            plans.append(p)

    m = MonthlyPlan()
    m.title = title
    m.startTime = startTime
    m.endTime = endTime
    m.plans = plans
    m.yearlyPlan = y
    m.save()
    return jsonify({'status': True, 'info': u'月计划添加成功'})

@bpAdmin.route("/timeManagementMonthlyPlanEdit/<id>",methods=['GET','POST'])
@login_required
def timeManagementMonthlyPlanEdit(id):
    m = MonthlyPlan.objects(id=id).first()
    if request.method == 'GET':
        levels = current_app.config['PLAN_LEVEL']
        yps = YearlyPlan.objects.order_by('-id')
        return render_template('admin/timeManagementMonthlyPlanEdit.html',
                               levels=levels, m=m, yps=yps,
                               startTime=str(m.startTime).split(' ')[0],
                               endTime=str(m.endTime).split(' ')[0])

    if request.method == 'POST':
        title = request.form['title']
        yearlyPlanId = request.form['yearlyPlanId']
        startTime = request.form['startTime']
        endTime = request.form['endTime']
        planLevel = request.form.getlist('planLevel[]')
        planTitle = request.form.getlist('planTitle[]')
        isDone = request.form.getlist('isDone[]')

        if not strLength(title, 1, 100):
            return jsonify({'status': False, 'info': u'请输入1-100个字符的月计划标题！'})
        if not startTime or not endTime:
            return jsonify({'status': False, 'info': u'请选择时间范围！'})

        startTime = strToDatetime('%s 00:00:00' % startTime)
        endTime = strToDatetime('%s 23:59:59' % endTime)
        if endTime <= startTime:
            return jsonify({'status': False, 'info': u'结束时间必须要晚于开始时间！'})

        y = YearlyPlan.objects(id=yearlyPlanId).first()
        # 时间范围判断
        # 月计划的时间范围必须在年计划的时间范围内
        if not (startTime >= y.startTime and endTime <= y.endTime):
            return jsonify({'status': False, 'info': u'月计划的时间范围必须在年计划的时间范围内！'})
        # 该年计划下的月计划时间范围不冲突
        mps = MonthlyPlan.objects(yearlyPlan=y)
        for i in mps:
            if i==m:continue
            if not (startTime >= i.endTime or endTime <= i.startTime):
                return jsonify({'status': False, 'info':u'月计划的时间范围（%s - %s）和“%s”的时间范围（%s - %s）冲突' %
                      (startTime, endTime, i.title, i.startTime, i.endTime)})

        plans = []
        for index, t in enumerate(planTitle):
            if len(t) > 0:
                p = Plan()
                p.title = t
                p.level = planLevel[index]
                if isDone[index] == 'y':
                    p.isDone = True
                else:
                    p.isDone = False
                plans.append(p)

        m.title = title
        m.startTime = startTime
        m.endTime = endTime
        m.plans = plans
        m.yearlyPlan = y
        m.save()
        return jsonify({'status': True, 'info': u'月计划修改成功！'})

@bpAdmin.route("/timeManagementMonthlyPlanDelete/<id>",methods=['GET'])
@login_required
def timeManagementMonthlyPlanDelete(id):
    # 有子计划不能删除
    p = MonthlyPlan.objects(id=id).first()
    if len(WeeklyPlan.objects(monthlyPlan=p)) > 0:
        flash(u'该月计划有下属周计划，不能删除，请先删除下属周计划后，再删除月计划')
    else:
        p.delete()
        flash(u'月计划删除成功')
    return redirect(url_for('admin.timeManagementMonthlyPlan'))
#月计划____________________________________________________________________________________________

#周计划____________________________________________________________________________________________
@bpAdmin.route("/timeManagementWeeklyPlan")
@login_required
def timeManagementWeeklyPlan():
    levels = current_app.config['PLAN_LEVEL']
    wps = WeeklyPlan.objects.order_by('-id')
    #只展示最近12个月
    mps = MonthlyPlan.objects.order_by('-id')[:12]
    return render_template('admin/timeManagementWeeklyPlan.html',
                           levels=levels,mps=mps,wps=wps)

@bpAdmin.route("/timeManagementWeeklyPlanAdd",methods=['POST'])
@login_required
def timeManagementWeeklyPlanAdd():
    title = request.form['title']
    monthlyPlanId = request.form['monthlyPlanId']
    startTime = request.form['startTime']
    endTime = request.form['endTime']
    planLevel = request.form.getlist('planLevel[]')
    planTitle = request.form.getlist('planTitle[]')

    if not strLength(title,1,100):
        return jsonify({'status': False, 'info': u'请输入1-100个字符的周计划标题！'})
    if not startTime or not endTime:
        return jsonify({'status': False, 'info': u'请选择时间范围！'})

    startTime = strToDatetime('%s 00:00:00' % startTime)
    endTime = strToDatetime('%s 23:59:59' % endTime)
    if endTime <= startTime:
        return jsonify({'status': False, 'info': u'结束时间必须要晚于开始时间！'})

    m = MonthlyPlan.objects(id=monthlyPlanId).first()
    #时间范围判断
    #周计划的时间范围必须在月计划的时间范围内
    if not (startTime>=m.startTime and endTime<=m.endTime):
        return jsonify({'status': False, 'info': u'周计划的时间范围必须在月计划的时间范围内！'})
    #该年计划下的月计划时间范围不冲突
    wps = WeeklyPlan.objects(monthlyPlan=m)
    for i in wps:
        if not (startTime >= i.endTime or endTime <= i.startTime):
            return jsonify({'status': False, 'info': u'周计划的时间范围（%s - %s）和“%s”的时间范围（%s - %s）冲突' %
                  (startTime,endTime,i.title,i.startTime,i.endTime)})

    plans = []
    for index, t in enumerate(planTitle):
        if len(t) > 0:
            p = Plan()
            p.title = t
            p.level = planLevel[index]
            plans.append(p)

    w = WeeklyPlan()
    w.title = title
    w.startTime = startTime
    w.endTime = endTime
    w.plans = plans
    w.monthlyPlan = m
    w.save()
    return jsonify({'status': True, 'info': u'周计划添加成功！'})

@bpAdmin.route("/timeManagementWeeklyPlanEdit/<id>",methods=['GET','POST'])
@login_required
def timeManagementWeeklyPlanEdit(id):
    w = WeeklyPlan.objects(id=id).first()
    if request.method == 'GET':
        levels = current_app.config['PLAN_LEVEL']
        mps = MonthlyPlan.objects.order_by('-id')[:12]
        return render_template('admin/timeManagementWeeklyPlanEdit.html',
                               levels=levels, w=w, mps=mps,
                               startTime=str(w.startTime).split(' ')[0],
                               endTime=str(w.endTime).split(' ')[0])

    if request.method == 'POST':
        title = request.form['title']
        monthlyPlanId = request.form['monthlyPlanId']
        startTime = request.form['startTime']
        endTime = request.form['endTime']
        planLevel = request.form.getlist('planLevel[]')
        planTitle = request.form.getlist('planTitle[]')
        isDone = request.form.getlist('isDone[]')

        if not strLength(title, 1, 100):
            return jsonify({'status': False, 'info': u'请输入1-100个字符的周计划标题！'})
        if not startTime or not endTime:
            return jsonify({'status': False, 'info': u'请选择时间范围！'})

        startTime = strToDatetime('%s 00:00:00' % startTime)
        endTime = strToDatetime('%s 23:59:59' % endTime)
        if endTime <= startTime:
            return jsonify({'status': False, 'info': u'结束时间必须要晚于开始时间！'})

        m = MonthlyPlan.objects(id=monthlyPlanId).first()
        # 时间范围判断
        # 周计划的时间范围必须在月计划的时间范围内
        if not (startTime >= m.startTime and endTime <= m.endTime):
            return jsonify({'status': False, 'info': u'周计划的时间范围必须在月计划的时间范围内！'})
        # 该月计划下的周计划时间范围不冲突
        wps = WeeklyPlan.objects(monthlyPlan=m)
        for i in wps:
            if i==w:continue
            if not (startTime >= i.endTime or endTime <= i.startTime):
                return jsonify({'status': False, 'info': u'周计划的时间范围（%s - %s）和“%s”的时间范围（%s - %s）冲突' %
                                (startTime, endTime, i.title, i.startTime, i.endTime)})

        plans = []
        for index, t in enumerate(planTitle):
            if len(t) > 0:
                p = Plan()
                p.title = t
                p.level = planLevel[index]
                if isDone[index] == 'y':
                    p.isDone = True
                else:
                    p.isDone = False
                plans.append(p)

        w.title = title
        w.startTime = startTime
        w.endTime = endTime
        w.plans = plans
        w.monthlyPlan = m
        w.save()
        return jsonify({'status': True, 'info': u'周计划修改成功！'})

@bpAdmin.route("/timeManagementWeeklyPlanDelete/<id>",methods=['GET'])
@login_required
def timeManagementWeeklyPlanDelete(id):
    # 有子计划不能删除
    p = WeeklyPlan.objects(id=id).first()
    if len(DailyPlan.objects(weeklyPlan=p)) > 0:
        flash(u'该周计划有下属日计划，不能删除，请先删除下属日计划后，再删除周计划')
    else:
        p.delete()
        flash(u'周计划删除成功')
    return redirect(url_for('admin.timeManagementWeeklyPlan'))
#周计划____________________________________________________________________________________________

#日计划____________________________________________________________________________________________
@bpAdmin.route("/timeManagementDailyPlan")
@login_required
def timeManagementDailyPlan():
    dps = DailyPlan.objects.order_by('-id')
    levels = current_app.config['PLAN_LEVEL']
    # 只展示最近12周
    wps = WeeklyPlan.objects.order_by('-id')[:12]
    return render_template('admin/timeManagementDailyPlan.html',
                           levels=levels,dps=dps,wps=wps)

@bpAdmin.route("/timeManagementDailyPlanAdd",methods=['POST'])
@login_required
def timeManagementDailyPlanAdd():
    weeklyPlanId = request.form['weeklyPlanId'].strip()
    whichDay = request.form['whichDay'].strip()
    planLevel = request.form.getlist('planLevel[]')
    planTitle = request.form.getlist('planTitle[]')
    print (planLevel)

    try:
        whichDayTemp = strToDatetime('%s 00:00:00' % whichDay)
    except:
        return jsonify({'status': False, 'info': u'请输入正确的时间格式！'})

    w = WeeklyPlan.objects(id=weeklyPlanId).first()
    #时间范围判断
    #日计划的时间范围必须在周计划的时间范围内
    if not (whichDayTemp>=w.startTime and whichDayTemp<=w.endTime):
        return jsonify({'status': False, 'info': u'日计划的时间范围必须在周计划的时间范围内！'})
    #该周计划下的日计划时间范围不冲突
    dps = DailyPlan.objects(weeklyPlan=w)
    for i in dps:
        if i.whichDay == whichDay:
            return jsonify({'status': False, 'info': u'该日期 “%s” 已经有日计划了！' % whichDay})

    plans = []
    for index, t in enumerate(planTitle):
        if len(t) > 0:
            p = Plan()
            p.title = t.strip()
            p.level = planLevel[index].strip()
            plans.append(p)

    d = DailyPlan()
    d.title = "%s日计划" % whichDay
    d.whichDay = whichDay
    d.plans = plans
    d.weeklyPlan = w
    d.save()
    return jsonify({'status': True, 'info': u'日计划添加成功！'})

@bpAdmin.route("/timeManagementDailyPlanEdit/<id>",methods=['GET','POST'])
@login_required
def timeManagementDailyPlanEdit(id):
    d = DailyPlan.objects(id=id).first()
    if request.method == 'GET':
        levels = current_app.config['PLAN_LEVEL']
        wps = WeeklyPlan.objects.order_by('-id')[:12]
        return render_template('admin/timeManagementDailyPlanEdit.html',
                               levels=levels, d=d, wps=wps)

    if request.method == 'POST':
        weeklyPlanId = request.form['weeklyPlanId'].strip()
        whichDay = request.form['whichDay'].strip()
        planLevel = request.form.getlist('planLevel[]')
        planTitle = request.form.getlist('planTitle[]')
        isDone = request.form.getlist('isDone[]')

        try:
            whichDayTemp = strToDatetime('%s 00:00:00' % whichDay)
        except:
            return jsonify({'status': False, 'info': u'请输入正确的时间格式！'})

        w = WeeklyPlan.objects(id=weeklyPlanId).first()
        # 时间范围判断
        # 日计划的时间范围必须在周计划的时间范围内
        if not (whichDayTemp >= w.startTime and whichDayTemp <= w.endTime):
            return jsonify({'status': False, 'info': u'日计划的时间范围必须在周计划的时间范围内！'})
        # 该周计划下的日计划时间范围不冲突
        dps = DailyPlan.objects(weeklyPlan=w)
        for i in dps:
            if d == i:continue
            if i.whichDay == whichDay:
                return jsonify({'status': False, 'info': u'该日期 “%s” 已经有日计划了！' % whichDay})

        plans = []
        for index, t in enumerate(planTitle):
            if len(t) > 0:
                p = Plan()
                p.title = t.strip()
                p.level = planLevel[index].strip()
                if isDone[index] == 'y':
                    p.isDone = True
                else:
                    p.isDone = False
                plans.append(p)

        d.title = "%s日计划" % whichDay
        d.whichDay = whichDay
        d.plans = plans
        d.weeklyPlan = w
        d.save()
        return jsonify({'status': True, 'info': u'日计划修改成功！'})

@bpAdmin.route("/timeManagementDailyPlanDelete/<id>",methods=['GET'])
@login_required
def timeManagementDailyPlanDelete(id):
    p = DailyPlan.objects(id=id).first()
    #同时删除该周计划下的日计划
    p.delete()
    flash(u'日计划删除成功')
    return redirect(url_for('admin.timeManagementDailyPlan'))

@bpAdmin.route("/timeManagementDailyTasksEdit",methods=['GET','POST'])
@login_required
def timeManagementDailyTasksEdit():
    if request.method == 'GET':
        levels = current_app.config['PLAN_LEVEL']
        return render_template('admin/timeManagementDailyTasksEdit.html',levels=levels)

    if request.method == 'POST':
        planLevel = request.form.getlist('planLevel[]')
        planTitle = request.form.getlist('planTitle[]')

        plans = []
        for index, t in enumerate(planTitle):
            if len(t) > 0:
                plans.append([planLevel[index].strip(),t.strip()])

        current_user.custom['dailyTasks'] = plans
        current_user.save()
        return jsonify({'status': True, 'info': u'日常修改成功！'})
#日计划____________________________________________________________________________________________
