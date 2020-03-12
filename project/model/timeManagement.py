# -*- coding: utf-8 -*-
# @Time    : 2019-12-24
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

from mongoengine import *

class Plan(EmbeddedDocument):
    title = StringField(max_length=1000, required=True)
    level = StringField(max_length=100, required=True)
    isDone = BooleanField(default=False)

class YearlyPlan(Document):
    title = StringField(max_length=1000, required=True)
    startTime = DateTimeField(required=True)
    endTime = DateTimeField(required=True)
    plans = ListField(EmbeddedDocumentField(Plan))
    doneCount = IntField(default=0)
    summarize = StringField(max_length=20000)

class MonthlyPlan(Document):
    title = StringField(max_length=1000, required=True)
    startTime = DateTimeField(required=True)
    endTime = DateTimeField(required=True)
    plans = ListField(EmbeddedDocumentField(Plan))
    doneCount = IntField(default=0)
    summarize = StringField(max_length=20000)
    yearlyPlan = ReferenceField(YearlyPlan)

class WeeklyPlan(Document):
    title = StringField(max_length=1000, required=True)
    startTime = DateTimeField(required=True)
    endTime = DateTimeField(required=True)
    plans = ListField(EmbeddedDocumentField(Plan))
    doneCount = IntField(default=0)
    summarize = StringField(max_length=20000)
    monthlyPlan = ReferenceField(MonthlyPlan)

class DailyPlan(Document):
    title = StringField(max_length=1000, required=True)
    whichDay = StringField(max_length=100, required=True)
    plans = ListField(EmbeddedDocumentField(Plan))
    doneCount = IntField(default=0)
    summarize = StringField(max_length=20000)
    weeklyPlan = ReferenceField(WeeklyPlan)


