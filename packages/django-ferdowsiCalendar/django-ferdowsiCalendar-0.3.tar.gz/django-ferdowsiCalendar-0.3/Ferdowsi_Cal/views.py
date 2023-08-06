
from django.http import  HttpResponse
from django.views.decorators.csrf import csrf_protect
from .models import CalEvents
from khayyam import *
import calendar
import json
import datetime
from django.contrib.auth.models import User
from django.shortcuts import render

def getGregorianMonth(request, year:int, month:int):
    if request.is_ajax and request.method == "GET":
        c = calendar.monthcalendar(year,month)
        events = []
        back_events = CalEvents.objects.filter(date__year=str(year),
                      date__month=str(month))

        for ev in back_events:
            users = list(ev.users.all())
            for u in range(0,len(users)):
                users[u] = users[u].username
            if len(users)>0:
                temp = {'name': ev.title,
                        'content': ev.content,
                        'day': ev.date.day,
                        'id' :ev.id,
                        'users': users
                        }
                events.append(temp)
    return HttpResponse(json.dumps({'cal':c,'events':events},ensure_ascii=False))


def getPersianMonth(request, year:int, month:int):
    if request.is_ajax and request.method == "GET":
        firstDayOfMonth = JalaliDatetime(year, month, 1)
        days = []
        days.append([])
        dayCounter = 1
        jmonth = month
        for i in range(1, firstDayOfMonth.isoweekday()):
            days[0].append(0)
        for i in range(firstDayOfMonth.isoweekday(), 8):
            days[0].append(dayCounter)
            dayCounter += 1
        limit = 31;
        if jmonth <= 6:
            limit = 31;
        elif jmonth <= 11:
            limit = 30
        elif firstDayOfMonth.isleap:
            limit = 30
        else:
            limit = 29
        finished = False
        for i in range(1, 7):
            days.append([])
            for j in range(7 * i + 1, 7 * (i + 1) + 1):
                if dayCounter > limit:
                    days[i].append(0);
                    finished = True
                else:
                    days[i].append(dayCounter)
                    dayCounter += 1
            if finished:
                break
        events = []

        for i in range(1, firstDayOfMonth.daysinmonth + 1):
            jday = JalaliDate(year, month, i)
            day = jday.todate()
            evs = CalEvents.objects.filter(date__year=str(day.year),
                                           date__month=str(day.month), date__day=str(day.day))
            for ev in evs:
                users = list(ev.users.all())
                for u in range(0, len(users)):
                    users[u] = users[u].username
                if len(users) > 0:
                    temp = {'name': ev.title,
                            'content': ev.content,
                            'day': i,
                            'id': ev.id,
                            'users': users
                            }
                    events.append(temp)
    return HttpResponse(json.dumps({'cal':days,'events':events},ensure_ascii=False))

@csrf_protect
def addEvent(request, name:str, content:str, year:int, month:int, day:int, users:str):
    d = datetime.date(year, month, day)
    event = CalEvents(title=name, content=content, date=d)
    event.save()
    u = users.split(',')
    for user in u:
        myUsers = User.objects.filter(username=user).first()
        event.users.add(myUsers)
    return HttpResponse(json.dumps({'suc':True},ensure_ascii=False))

@csrf_protect
def addPersianEvent(request, name:str, content:str, year:int, month:int, day:int, users:str):
    d = JalaliDate(year, month, day).todate()
    event = CalEvents(title=name, content=content, date=d)
    event.save()
    u = users.split(',')
    for user in u:
        myUsers = User.objects.filter(username=user).first()
        event.users.add(myUsers)
    return HttpResponse(json.dumps({'suc':True},ensure_ascii=False))



@csrf_protect
def editEvent(request, name:str, content:str, year:int, month:int, day:int, id:int, users:str):
    d = datetime.date(year, month, day)
    event = CalEvents.objects.get(id=id)
    event.title = name;
    event.content = content;
    event.date = d;
    event.save()
    uu = User.objects.all()
    for uuu in uu:
        event.users.remove(uuu)
    u = users.split(',')
    for user in u:
        myUsers = User.objects.filter(username=user).first()
        event.users.add(myUsers)
    return HttpResponse(json.dumps({'suc':True},ensure_ascii=False))

@csrf_protect
def editPersianEvent(request, name:str, content:str, year:int, month:int, day:int, id:int, users:str):
    d = JalaliDate(year, month, day).todate()
    event = CalEvents.objects.get(id=id)
    event.title = name;
    event.content = content;
    event.date = d;
    event.save()
    uu = User.objects.all()
    for uuu in uu:
        event.users.remove(uuu)
    u = users.split(',')
    for user in u:
        myUsers = User.objects.filter(username=user).first()
        event.users.add(myUsers)
    return HttpResponse(json.dumps({'suc':True},ensure_ascii=False))


@csrf_protect
def deleteEvent(request, id:int):
    instance = CalEvents.objects.get(id=id)
    instance.delete()
    return HttpResponse(json.dumps({'suc':True},ensure_ascii=False))


