from core.utils import add_dir, del_dir
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
import hashlib

from bots.forms import BotForm, BotFormEdit, BotPass, BotSchedule
from bots.models import Bot
from main_bot.main_classes import BotData
from users.models import AdminBot


def index(request):
    cur_admin = get_object_or_404(AdminBot, tgid=request.COOKIES.get('chatid'))
    bots = cur_admin.bot.all()
    return render(request, 'index.html', {'bots': bots, })


def bot(request, botid):
    return render(request, 'bots/bots.html')


def botdel(request, botid):
    cur_bot = get_object_or_404(Bot, id=botid)
    bot = BotData(cur_bot.token)
    bot.delete_webhook()
    cur_bot.delete()
    messages.success(request, 'Бот удалён')
    del_dir(botid=botid, type_dir='bot')
    return redirect('bots:index')


def botpass(request, botid):
    if request.method != "POST":
        return render(request, 'bots/botpass.html', {'form': BotPass, })
    Bot.objects.filter(id=botid).update(
        password=hashlib.md5(request.POST['password'].encode()))
    messages.success(request, 'Пароль бота установлен.')
    return redirect('bots:bot_page', botid=botid)


def botedit(request, botid):
    cur_bot = get_object_or_404(Bot, id=botid)
    form = BotFormEdit(request.POST or None, instance=cur_bot)
    if form.is_valid():
        form.save()
        messages.success(request, 'Бот отредактирован.')
        return redirect('bots:bot_page', botid=cur_bot.id)
    if request.method == "POST":
        messages.error(request, ' ')
    return render(request, 'bots/botadd.html', {'form': form, })


def botadd(request):
    form = BotForm(request.POST or None)
    if not form.is_valid():
        context = {
            'form': form,
            'is_new': True,
        }
        if request.method == "POST":
            messages.error(request, ' ')
        return render(request, 'bots/botadd.html', context)
    new_bot = form.save(commit=False)
    new_bot.id = int((request.POST['token'].split(':'))[0])
    new_bot.admin = get_object_or_404(
        AdminBot, tgid=request.COOKIES.get('chatid'))
    form.save()
    add_dir(botid=new_bot.id)
    messages.success(request, 'Бот добавлен.')
    return redirect('bots:bot_page', botid=new_bot.id)


def botrunstop(request, botid):
    cur_bot = get_object_or_404(Bot, id=botid)
    active_categories = cur_bot.category.filter(is_active=True)

    if not (cur_bot.days and cur_bot.hours):
        messages.error(request, 'Необходимо настроить расписание.')
        return redirect('bots:bot_schedule', botid=botid)
    if not active_categories:
        messages.error(request, 'Необходимо включить хотя бы одну категорию.')
        return redirect('tasks:category', botid=botid)

    Bot.objects.filter(id=botid).update(is_active=not cur_bot.is_active)
    if cur_bot.is_active:
        messages.success(request, 'Бот остановлен.')
    else:
        messages.success(request, 'Бот запущен.')
    return redirect('bots:bot_page', botid=botid)


def botschedule(request, botid):
    cur_bot = get_object_or_404(Bot, id=botid)
    form = BotSchedule(request.POST or None, instance=cur_bot)
    if form.is_valid():
        form.save()
        messages.success(request, 'Расписание изменено.')
        return redirect('bots:bot_page', botid=cur_bot.id)
    if request.method == "POST":
        messages.error(request, ' ')
    return render(request, 'bots/botschedule.html', {'form': form, })
