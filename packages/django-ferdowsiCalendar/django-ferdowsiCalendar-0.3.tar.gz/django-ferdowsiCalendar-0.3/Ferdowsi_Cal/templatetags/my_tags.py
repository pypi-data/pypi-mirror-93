from django import template
from django.apps import apps
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.template.loader import render_to_string
import calendar
from datetime import datetime
from khayyam import *

from Ferdowsi_Cal.models import CalEvents

register = template.Library()

@register.simple_tag()
def Gregorian_calendar(admin):
    today = datetime.today()
    c = calendar.monthcalendar(today.year, today.month)
    events = []
    back_events = CalEvents.objects.filter(date__year=str(today.year),
                      date__month=str(today.month))
    for ev in back_events:

        ev_users = list(ev.users.all())
        for u in range(0, len(ev_users)):
            ev_users[u] = ev_users[u].username
        if len(ev_users) > 0:
            temp = {'name': ev.title,
                    'content': ev.content,
                    'day': ev.date.day,
                    'id' :ev.id,
                    'ev_users': ev_users
                    }
            events.append(temp)

    users = User.objects.all()
    data = {'cal': c,
            'events': events,
            'year': today.year,
            'month': calendar.month_name[today.month],
            'today': today.day,
            'users': users
            }
    if admin:
        output = render_to_string('Ferdowsi_Cal/gregorian_calendar.html', data)
    else:
        output = render_to_string('Ferdowsi_Cal/gregorian_calendar_user.html', data)
    return format_html(output)



@register.simple_tag()
def Persian_calendar(admin):
    today = datetime.today()
    jtoday = JalaliDatetime(today)
    firstDayOfMonth = JalaliDatetime(jtoday.year,jtoday.month,1)


    users = User.objects.all()
    events = []

    for i in range(1,jtoday.daysinmonth+1):
        jday = JalaliDate(jtoday.year,jtoday.month,i)
        day = jday.todate()
        evs = CalEvents.objects.filter(date__year=str(day.year),
                                               date__month=str(day.month),date__day=str(day.day))
        for ev in evs:
            ev_users = list(ev.users.all())
            for u in range(0, len(ev_users)):
                ev_users[u] = ev_users[u].username
            if len(ev_users)>0:
                temp = {'name': ev.title,
                        'content': ev.content,
                        'day': i,
                        'id': ev.id,
                        'ev_users':ev_users
                        }
                events.append(temp)

    days=[]
    days.append([])
    dayCounter = 1
    jmonth = jtoday.month
    for i in range(1,firstDayOfMonth.isoweekday()):
        days[0].append(0)
    for i in range(firstDayOfMonth.isoweekday(),8):
        days[0].append(dayCounter)
        dayCounter += 1
    limit = 31;
    if jmonth<=6:
        limit = 31;
    elif jmonth<=11:
        limit = 30
    elif firstDayOfMonth.isleap:
        limit = 30
    else:
        limit = 29
    finished = False
    for i in range(1,7):
        days.append([])
        for j in range(7*i+1,7*(i+1)+1):
            if dayCounter>limit:
                days[i].append(0);
                finished = True
            else:
                days[i].append(dayCounter)
                dayCounter += 1
        if finished:
            break
    data = {'cal': days,
            'events':events,
            'year': jtoday.year,
            'month': jtoday.month,
            'monthName': jtoday.monthname(),
            'today': jtoday.day,
            'users': users
            }
    if admin:
        output = render_to_string('Ferdowsi_Cal/persian_calendar.html', data)
    else:
        output = render_to_string('Ferdowsi_Cal/persian_calendar_user.html', data)
    return format_html(output)

@register.simple_tag()
def Diagram(app, model, column, fkey):
    myModel = apps.get_model(app, model)
    columns = myModel.objects.values_list(fkey,column).all()
    users = User.objects.all()
    user_fields = []
    for u in users:
        ev_count = u.calevents_set.all().count()
        temp = {}
        temp['u'] = u.username
        temp['c'] = ev_count
        temp['f'] = 0
        for f in columns:
            if u.id == f[0]:
                temp['f'] = f[1]
        user_fields.append(temp)
    data = {
        'user_fields':user_fields,
        'column':column
    }
    output = render_to_string('Ferdowsi_Cal/diagram.html', data)
    return format_html(output)

