from django.shortcuts import get_object_or_404, render

from stats.clndr import (
    dates_tz, form_processing, get_dates_from_coockies, new_date_form
)
from content.models import Category, Log, Task
from stats.forms import SelectDateForm_disabled
from stats.functions import compare_logs, get_stats
from users.models import Student


def task(request, botid, task_id):
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
    tasks = Task.objects.filter(category__id=cat_id).filter(time__gte='2020-01-01 00:00:01')
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
    cat_stats = get_stats(tasks, dates, student) if tasks else {}
    stud_stats = get_stats(students, dates, student) if students else {}
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
    student = get_object_or_404(Student, id=user_id) if user_id != 'all' else None
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
                task_count = tasks.filter(time__gte='2020-01-01 00:00:01').count()
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
            logs = Log.objects.filter(category=category).filter(student=student)
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
                task_count = tasks.filter(time__gte='2020-01-01 00:00:01').count()
                stats[category.id] = [task_count, 0, 0, 0]
                compare_logs(stats, logs, category.id, 0)
    context = {
        'categories': categories,
        'stats': stats,
        'form': new_date_form(start_end_date),
        'student': student,
        'pin': pin
    }
    return render(request, 'stats/userstat.html', context)


def usercatstat(request, botid, user_id, cat_id, pin):
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
    tasks = Task.objects.filter(category__id=cat_id).filter(time__gte='2020-01-01 00:00:01')
    dates = None
    if start_end_date:
        dates = dates_tz(start_end_date, botid)
        tasks = tasks.filter(
            time__gte=dates[0],
            time__lte=dates[1],
        )
    cat_stats = get_stats(tasks, dates, student) if tasks else {}
    context = {
        'task_count': tasks.count(),
        'tasks': tasks,
        'cat_stats': cat_stats,
        'category': get_object_or_404(Category, id=cat_id),
        'form': new_date_form(start_end_date),
        'student': student,
        'pin': pin
    }
    return render(request, 'stats/usercatstat.html', context)
