from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from bots.models import Bot
from content.forms import CategoryForm, TaskForm
from content.functions import is_need_stop_bot
from content.models import Category, Task
from content.permissions import can_category_run
from content.utils import get_paginator
from core.utils import add_dir, del_dir, del_file, replace_from_temp


def category(request, botid):
    """Категории текущего бота."""
    cur_bot = get_object_or_404(Bot, id=botid)
    categories = cur_bot.category.all()
    context = {
        'categories': categories,
        'widget': 'category',
    }
    return render(request, 'content/categories.html', context)


def categoryadd(request, botid):
    """Добавляем категорию."""
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        return categoryadd_done(request, botid, form)
    context = {
        'form': form,
        'is_new': True,
    }
    if request.method == "POST":
        messages.error(request, ' ')
    return render(request, 'content/categoryadd.html', context)


def categoryadd_done(request, botid, form):
    """Сохраняем форму добавления категории."""
    new_category = form.save(commit=False)
    new_category.bot = get_object_or_404(Bot, id=botid)
    form.save()
    add_dir(botid=botid, num_dir=new_category.id, type_dir='cat')
    messages.success(request, 'Категория добавлена.')
    return redirect('content:category', botid=botid)


def categoryedit(request, botid, categoryid):
    """Редактируем категорию."""
    cur_category = get_object_or_404(Category, id=categoryid)
    form = CategoryForm(request.POST or None, instance=cur_category)
    if form.is_valid():
        form.save()
        messages.success(request, 'Категория изменена.')
        return redirect('content:category', botid=botid)
    context = {
        'form': form,
        'is_new': False,
    }
    if request.method == "POST":
        messages.error(request, ' ')
    return render(request, 'content/categoryadd.html', context)


def categorydel(request, botid, categoryid):
    """Удаляем категорию."""
    Category.objects.filter(id=categoryid).delete()
    del_dir(botid=botid, num_dir=categoryid, type_dir='cat')
    is_need_stop_bot(botid)
    messages.success(request, 'Категория удалена.')
    return redirect('content:category', botid=botid)


def categorytasks(request, botid, categoryid):
    """Задания текущей категории."""
    cur_category = get_object_or_404(Category, id=categoryid)
    tasks = cur_category.task.all()
    page_obj = get_paginator(request, tasks)
    context = {
        'category_name': tasks.__dict__['_hints']['instance'],
        'page_obj': page_obj,
        'category_id': categoryid,
        'widget': 'task',
    }
    return render(request, 'content/category_tasks.html', context)


def taskadd(request, botid, categoryid):
    """Добавляем задание."""
    form = TaskForm(request.POST, request.FILES or None)
    if not form.is_valid():
        if request.method == "POST":
            messages.error(request, ' ')
        return render(request, 'content/taskadd.html', {'form': form})
    new_task = form.save(commit=False)
    new_task.category = get_object_or_404(Category, id=categoryid)
    new_task.bot = get_object_or_404(Bot, id=botid)
    form.save()
    if request.FILES:
        name_new = replace_from_temp(
            botid=botid, num_file=new_task.id, type_dir='cat',
            num_dir=categoryid, img_name=request.FILES['img']._name)
        Task.objects.filter(id=new_task.id).update(img='/'.join(
            [str(botid), f'cat{categoryid}', name_new]))
    messages.success(request, 'Задача добавлена.')
    return redirect(
        'content:category_tasks', botid=botid, categoryid=categoryid)


def task(request, botid, categoryid, taskid):
    """Информация о задании."""
    cur_bot = get_object_or_404(Bot, id=botid)
    cur_task = get_object_or_404(Task, id=taskid)
    context = {
        'task': cur_task,
        'categoryid': categoryid,
        'tz': cur_bot.tz,
    }
    return render(request, 'content/task.html', context)


def taskedit(request, botid, categoryid, taskid):
    """Редактируем задание."""
    cur_task = get_object_or_404(Task, id=taskid)
    img_url = cur_task.img
    form = TaskForm(request.POST, request.FILES or None, instance=cur_task)
    if not form.is_valid():
        if request.method == "POST":
            messages.error(request, ' ')
        context = {
            'form': form,
            'task': cur_task,
        }
        return render(request, 'content/taskedit.html', context)
    if request.FILES and img_url or request.POST.get('img-clear', False):
        del_file(url=img_url)
    form.save()
    if request.FILES:
        name_new = replace_from_temp(
            botid=botid, num_file=taskid, type_dir='cat',
            num_dir=categoryid, img_name=request.FILES['img']._name)
        Task.objects.filter(id=taskid).update(img='/'.join(
            [str(botid), f'cat{categoryid}', name_new]))
    messages.success(request, 'Задача отредактирована.')
    return redirect(
        'content:task', botid=botid, categoryid=categoryid, taskid=taskid)


def taskdel(request, botid, categoryid, taskid):
    """Удаляем задание."""
    cur_task = Task.objects.get(id=taskid)
    if cur_task.img:
        del_file(url=cur_task.img)
    Task.objects.filter(id=taskid).delete()
    messages.success(request, 'Задание удалено.')
    return redirect(
        'content:category_tasks', botid=botid, categoryid=categoryid)


def catrunstop(request, botid, categoryid):
    """Запускаем или останавливаем категорию."""
    cur_category = get_object_or_404(Category, id=categoryid)
    permission = can_category_run(cur_category)
    if permission[0] > 1:
        messages.error(request, permission[1])
        return redirect(permission[2], botid=botid, categoryid=categoryid)

    Category.objects.filter(id=categoryid).update(
        is_active=not cur_category.is_active)
    if cur_category.is_active:
        is_need_stop_bot(botid)
        messages.success(request, 'Категория остановлена.')
    else:
        messages.success(request, 'Категория запущена.')
    return redirect('content:category', botid=botid)
