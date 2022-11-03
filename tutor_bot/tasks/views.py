from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from bots.models import Bot
from core.utils import add_dir, del_dir, del_file, replace_from_temp
from tasks.forms import CategoryForm, TaskForm
from tasks.models import Category, Task


def category(request, botid):
    cur_bot = get_object_or_404(Bot, id=botid)
    categories = cur_bot.category.all()
    context = {
        'categories': categories,
        'widget': 'category',
    }
    return render(request, 'tasks/categories.html', context)


def categoryadd(request, botid):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        new_category = form.save(commit=False)
        new_category.bot = get_object_or_404(Bot, id=botid)
        form.save()
        add_dir(botid=botid, num_dir=new_category.id, type_dir='cat')
        messages.success(request, 'Категория добавлена.')
        return redirect('tasks:category', botid=botid)
    context = {
        'form': form,
        'is_new': True,
    }
    if request.method == "POST":
        messages.error(request, ' ')
    return render(request, 'tasks/categoryadd.html', context)


def categoryedit(request, botid, categoryid):
    cur_category = get_object_or_404(Category, id=categoryid)
    form = CategoryForm(request.POST or None, instance=cur_category)
    if form.is_valid():
        form.save()
        messages.success(request, 'Категория изменена.')
        return redirect('tasks:category', botid=botid)
    context = {
        'form': form,
        'is_new': False,
    }
    if request.method == "POST":
        messages.error(request, ' ')
    return render(request, 'tasks/categoryadd.html', context)


def categorydel(request, botid, categoryid):
    Category.objects.filter(id=categoryid).delete()
    del_dir(botid=botid, num_dir=categoryid, type_dir='cat')
    messages.success(request, 'Категория удалена.')
    return redirect('tasks:category', botid=botid)


def categoryrunstop(request, botid, categoryid):
    cur_category = get_object_or_404(Category, id=categoryid)
    Category.objects.filter(id=categoryid).update(
        is_active=not cur_category.is_active)
    if cur_category.is_active:
        messages.success(request, 'Категория остановлена.')
    else:
        messages.success(request, 'Категория запущена.')
    return redirect('tasks:category', botid=botid)


def categorytasks(request, botid, categoryid):
    cur_category = get_object_or_404(Category, id=categoryid)
    tasks = cur_category.task.all()
    context = {
        'category_name': tasks.__dict__['_hints']['instance'],
        'tasks': tasks,
        'category_id': categoryid,
        'widget': 'task',
    }
    return render(request, 'tasks/category_tasks.html', context)


def taskadd(request, botid, categoryid):
    form = TaskForm(request.POST, request.FILES or None)
    if not form.is_valid():
        if request.method == "POST":
            messages.error(request, ' ')
        return render(request, 'tasks/taskadd.html', {'form': form})
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
    return redirect('tasks:category_tasks', botid=botid, categoryid=categoryid)


def task(request, botid, categoryid, taskid):
    cur_task = get_object_or_404(Task, id=taskid)
    context = {
        'task': cur_task,
        'categoryid': categoryid,
    }
    return render(request, 'tasks/task.html', context)


def taskedit(request, botid, categoryid, taskid):
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
        return render(request, 'tasks/taskedit.html', context)
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
        'tasks:task', botid=botid, categoryid=categoryid, taskid=taskid)


def taskdel(request, botid, categoryid, taskid):
    cur_task = Task.objects.get(id=taskid)
    if cur_task.img:
        del_file(url=cur_task.img)
    Task.objects.filter(id=taskid).delete()
    messages.success(request, 'Задание удалено.')
    return redirect(
        'tasks:category_tasks', botid=botid, categoryid=categoryid)
