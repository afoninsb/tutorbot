import contextlib
import hashlib
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from bots.forms import BotForm, BotFormEdit, BotPass, BotSchedule
from bots.models import Bot
from bots.permissions import can_bot_run
from core.utils import add_dir, del_dir
from edubot.main_classes import BotData
from tarifs.models import Tarif
from users.models import AdminBot, Student, StudentBot


def index(request):
    try:
        cur_admin = get_object_or_404(
            AdminBot, tgid=request.COOKIES.get('chatid'))
    except Exception:
        return HttpResponseForbidden()
    bots = cur_admin.bot.all()
    return render(request, 'index.html', {'bots': bots, })


def bot(request, botid):
    return render(request, 'bots/bots.html')


def botdel(request, botid):
    cur_bot = get_object_or_404(Bot, id=botid)
    bot = BotData(cur_bot.token)
    bot.delete_webhook()
    cur_bot.delete()
    del_dir(botid=botid, type_dir='bot')
    messages.success(request, 'Бот удалён')
    return redirect('bots:index')


def botpass(request, botid):
    if request.method != "POST":
        return render(request, 'bots/botpass.html', {'form': BotPass, })
    password = hashlib.pbkdf2_hmac(
        'sha256',
        request.POST['password'].encode('utf-8'),
        b'',
        100000,
        dklen=128
    )
    Bot.objects.filter(id=botid).update(
        # password=hashlib.md5(str(request.POST['password']).encode()))
        password=password)

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
    tgid = request.COOKIES.get('chatid')
    admin = get_object_or_404(AdminBot, tgid=tgid)
    new_bot.admin = admin
    if free_tarif := Tarif.objects.filter(duration=Tarif.TarifsTypes.FREE):
        new_bot.tarif = free_tarif[0]
    else:
        tarif = Tarif.objects.all()
        new_bot.tarif = tarif[0]
    form.save()
    with contextlib.suppress(IntegrityError):
        Student.objects.create(
            tgid=tgid,
            first_name=admin.first_name,
            last_name=admin.last_name,
        )
    StudentBot(
        bot=new_bot,
        student=Student.objects.get(tgid=tgid),
        is_activated=True
    ).save()
    add_dir(botid=new_bot.id)
    messages.success(
        request, 'Бот добавлен. Вы также добавлены в учащихся этого бота.')
    return redirect('bots:bot_page', botid=new_bot.id)


def botrunstop(request, botid):
    cur_bot = get_object_or_404(Bot, id=botid)
    permission = can_bot_run(cur_bot)
    if permission[0] > 1:
        messages.error(request, permission[1])
        if permission[0] in (2, 5):
            return redirect(permission[2])
        return redirect(permission[2], botid=botid)

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
