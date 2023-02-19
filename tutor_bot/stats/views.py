import json

from datetime import date, datetime, timedelta
from django.shortcuts import get_object_or_404, render

from bots.models import Bot
from content.models import Category, Log, Task
from stats.clndr import (dates_tz, form_processing, get_dates_from_coockies,
                         new_date_form)
from stats.forms import DateForm, SelectDateForm_disabled
from stats.functions import compare_logs, get_stats
from stats.models import Rating
from users.models import Student


def userchart(request, botid, user_id):
    queryset = Rating.objects.filter(
        bot_id=botid, student_id=user_id).order_by(
            'time').select_related('student')[:30]
    title = f'Прирост баллов посуточно за месяц: {queryset.first().student}'
    context = {
        'chartData': json.dumps(list(queryset.values_list('time', 'score')),
                                default=str),
        'title': title,
    }
    return render(request, 'stats/userchart.html', context)


def task(request, botid, task_id):
    """Статистика по заданию."""
    form = SelectDateForm_disabled(request.POST or None)
    if request.method == "POST":
        return form_processing(
            request,
            form,
            'stats/task.html',
            'stats:task',
            botid=botid,
            task_id=task_id,
        )
    start_end_date = get_dates_from_coockies(request)
    logs = Log.objects.filter(
        task__id=task_id).select_related('task').select_related('student')
    context = {
        'task': logs[0].task,
        'logs': logs,
        'form': new_date_form(start_end_date),
    }
    return render(request, 'stats/task.html', context)


def category(request, botid, cat_id, user_id):
    """Статистика по категории."""
    form = SelectDateForm_disabled(request.POST or None)
    if request.method == "POST":
        return form_processing(
            request,
            form,
            'stats/category.html',
            'stats:category',
            botid=botid,
            cat_id=cat_id,
            user_id=user_id,
        )
    start_end_date = get_dates_from_coockies(request)
    tasks = Task.objects.filter(category__id=cat_id).\
        filter(time__gte='2020-01-01 00:00:01')
    dates = None
    if start_end_date:
        dates = dates_tz(start_end_date, botid)
        tasks = tasks.filter(
            time__gte=dates[0],
            time__lte=dates[1],
        )
    if user_id != 'all':
        student = get_object_or_404(Student, id=user_id)
        students = None
    else:
        student = None
        students = Student.objects.filter(
            bot__id=botid).prefetch_related('log')
    cat_stats = get_stats(
        tasks, dates, student, cat_id) if tasks else {}
    stud_stats = get_stats(
        students, dates, student, cat_id) if students else {}
    context = {
        'task_count': tasks.count(),
        'tasks': tasks,
        'cat_stats': cat_stats,
        'stud_stats': stud_stats,
        'category': get_object_or_404(Category, id=cat_id),
        'form': new_date_form(start_end_date),
        'student': student,
        'students': students,
    }
    return render(request, 'stats/category.html', context)


def all_categories(request, botid, user_id):
    """Сводная статистика по всем категориям."""
    form = SelectDateForm_disabled(request.POST or None)
    if request.method == "POST":
        return form_processing(
            request,
            form,
            'stats/all_categories.html',
            'stats:all_categories',
            botid=botid,
            user_id=user_id,
        )
    start_end_date = get_dates_from_coockies(request)
    categories = Category.objects.filter(bot__id=botid)
    stats = {}
    student = get_object_or_404(
        Student, id=user_id) if user_id != 'all' else None
    if categories:
        for category in categories:
            tasks = Task.objects.filter(category=category)
            logs = Log.objects.filter(category=category)
            if student:
                logs = logs.filter(student=student)
            if logs and tasks:
                if start_end_date:
                    dates = dates_tz(start_end_date, botid)
                    logs = logs.filter(
                        time__gte=dates[0],
                        time__lte=dates[1],
                    )
                    tasks = tasks.filter(
                        time__gte=dates[0],
                        time__lte=dates[1],
                    )
                task_count = tasks.\
                    filter(time__gte='2020-01-01 00:00:01').count()
                stats[category.id] = [task_count, 0, 0, 0]
                compare_logs(stats, logs, category.id, 0)
    context = {
        'categories': categories,
        'stats': stats,
        'form': new_date_form(start_end_date),
        'student': student
    }
    return render(request, 'stats/all_categories.html', context)


def userstat(request, botid, user_id, pin):
    """Статистика пользователя обобщенная - переход из бота."""
    student = get_object_or_404(Student, id=user_id)
    if pin != student.pin:
        return render(request, '404.html')
    form = SelectDateForm_disabled(request.POST or None)
    if request.method == "POST":
        return form_processing(
            request,
            form,
            'stats/userstat.html',
            'stats:userstat',
            botid=botid,
            user_id=user_id,
            pin=pin
        )
    start_end_date = get_dates_from_coockies(request)
    categories = Category.objects.filter(bot__id=botid)
    stats = {}
    if categories:
        for category in categories:
            tasks = Task.objects.filter(category=category)
            logs = Log.objects.filter(category=category).\
                filter(student=student)
            if logs and tasks:
                if start_end_date:
                    dates = dates_tz(start_end_date, botid)
                    logs = logs.filter(
                        time__gte=dates[0],
                        time__lte=dates[1],
                    )
                    tasks = tasks.filter(
                        time__gte=dates[0],
                        time__lte=dates[1],
                    )
                task_count = tasks.\
                    filter(time__gte='2020-01-01 00:00:01').count()
                stats[category.id] = [task_count, 0, 0, 0]
                compare_logs(stats, logs, category.id, 0)
    context = {
        'botid': botid,
        'categories': categories,
        'stats': stats,
        'form': new_date_form(start_end_date),
        'student': student,
        'pin': pin
    }
    return render(request, 'stats/userstat.html', context)


def usercatstat(request, botid, user_id, cat_id, pin):
    """Статистика пользователя по категории - переход из бота."""
    student = get_object_or_404(Student, id=user_id)
    if pin != student.pin:
        return render(request, '404.html')
    form = SelectDateForm_disabled(request.POST or None)
    if request.method == "POST":
        return form_processing(
            request,
            form,
            'stats/usercatstat.html',
            'stats:usercatstat',
            botid=botid,
            cat_id=cat_id,
            user_id=user_id,
            pin=pin
        )
    start_end_date = get_dates_from_coockies(request)
    tasks = Task.objects.filter(category__id=cat_id).\
        filter(time__gte='2020-01-01 00:00:01')
    dates = None
    if start_end_date:
        dates = dates_tz(start_end_date, botid)
        tasks = tasks.filter(
            time__gte=dates[0],
            time__lte=dates[1],
        )
    cat_stats = get_stats(tasks, dates, student, cat_id) if tasks else {}
    context = {
        'botid': botid,
        'task_count': tasks.count(),
        'tasks': tasks,
        'cat_stats': cat_stats,
        'category': get_object_or_404(Category, id=cat_id),
        'form': new_date_form(start_end_date),
        'student': student,
        'pin': pin
    }
    return render(request, 'stats/usercatstat.html', context)


def rating(request, botid):
    """Отображение рейтинга."""
    if request.method == "POST":
        form = DateForm(request.POST)
        cur_date = date(
            int(request.POST['date_year']),
            int(request.POST['date_month']),
            int(request.POST['date_day'])
        )
    else:
        cur_date = datetime.now()
        data = {
            'date': date(cur_date.year, cur_date.month, cur_date.day),
        }
        form = DateForm(initial=data)
    delta_date = (cur_date - timedelta(days=7)).strftime('%Y-%m-%d')
    cur_date = cur_date.strftime('%Y-%m-%d')
    cur_bot = get_object_or_404(Bot, id=botid)
    rating_data = Rating.objects.filter(bot=cur_bot).\
        filter(time=cur_date).select_related('student')
    rating_data_delta = Rating.objects.filter(bot=cur_bot).\
        filter(time=delta_date).select_related('student')
    rating = {rtng.student: [rtng.score, 0] for rtng in rating_data}
    for rtng in rating_data_delta:
        if rtng.student in rating:
            rating[rtng.student][1] = rating[rtng.student][0] - rtng.score
    context = {
        'rating': rating,
        'form': form,
    }
    return render(request, 'stats/rating.html', context)
