import calendar
from datetime import date, datetime, timedelta
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from bots.models import Bot
from stats.forms import SelectDateForm, SelectDateForm_disabled


def now():
    return datetime.now()


def weekdaynow():
    moment = now()
    return calendar.weekday(moment.year, moment.month, moment.day)


def startdate(date):
    date = str(date).split(" ")[0]
    return f'{date} 00:00:00'


def enddate(date):
    date = str(date).split(" ")[0]
    return f'{date} 23:59:59'


def currentweek(*args):
    moment = now()
    date_start = moment - timedelta(days=weekdaynow())
    return (startdate(date_start), enddate(moment))


def previousweek(*args):
    date_end = now() - timedelta(days=(weekdaynow()+1))
    date_start = date_end - timedelta(days=6)
    return (startdate(date_start), enddate(date_end))


def currentmonth(*args):
    moment = now()
    date_start = str(datetime(moment.year, moment.month, 1))
    return (date_start, enddate(moment))


def previousmonth(*args):
    moment = now()
    pre = moment - timedelta(days=(moment.day+1))
    date_start = str(datetime(pre.year, pre.month, 1))
    num_days = calendar.monthrange(pre.year, pre.month)[1]
    date_end = enddate(datetime(pre.year, pre.month, num_days))
    return (date_start, date_end)


def other(request):
    date_start = date(
        int(request.POST['date_start_year']),
        int(request.POST['date_start_month']),
        int(request.POST['date_start_day'])
    ).strftime('%Y-%m-%d')
    date_end = date(
        int(request.POST['date_end_year']),
        int(request.POST['date_end_month']),
        int(request.POST['date_end_day'])
    ).strftime('%Y-%m-%d')
    return (f"{date_start} 00:00:00", f"{date_end} 23:59:59")


def allperiod(request):
    return ('', '')


def get_dates(request):
    period_func = {
        'allperiod': allperiod,
        'previousmonth': previousmonth,
        'currentmonth': currentmonth,
        'previousweek': previousweek,
        'currentweek': currentweek,
        'other': other
    }
    start_end = period_func[request.POST['period']](request)
    return '#'.join(start_end)


def new_date_form(start_end_date):
    if not start_end_date:
        return SelectDateForm_disabled()
    start_date = start_end_date[0].split(' ')[0].split('-')
    end_date = start_end_date[1].split(' ')[0].split('-')
    data = {
        'period': 'other',
        'date_start': date(
            int(start_date[0]), int(start_date[1]), int(start_date[2])),
        'date_end': date(
            int(end_date[0]), int(end_date[1]), int(end_date[2])),
    }
    return SelectDateForm(initial=data)


def form_processing(request, form, template, url, **kwargs):
    if not form.is_valid():
        messages.error(request, ' ')
        context = {'form': form}
        return render(request, template, context)
    response = redirect(url, **kwargs)
    start_end_date = get_dates(request)
    if start_end_date == '#':
        response.delete_cookie('dates')
    else:
        response.set_cookie(
            key='dates',
            value=start_end_date,
            secure=True,
            max_age=36000
        )
    return response


def get_dates_from_coockies(request):
    if start_end_date := request.COOKIES.get('dates'):
        return start_end_date.split('#')


def dates_tz(dates, botid):
    cur_bot = get_object_or_404(Bot, id=botid)
    tz = int(cur_bot.TimeZones(cur_bot.tz).label.split()[1])
    return (
        datetime.strptime(dates[0], '%Y-%m-%d %H:%M:%S') - timedelta(hours=tz),
        datetime.strptime(dates[1], '%Y-%m-%d %H:%M:%S') - timedelta(hours=tz)
    )
