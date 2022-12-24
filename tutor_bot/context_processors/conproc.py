import pytz
from datetime import datetime, timedelta
from django.conf import settings

from bots.models import Bot
from users.models import AdminBot

IGNORE_URL = (
    '/tgbot_backend',
    '/webhook',
    '/admin',
    'stats/user/',
    '/favicon.ico',
)


def is_continue(path) -> bool:
    return all(url not in path for url in IGNORE_URL)


def get_context_data(request):
    if not is_continue(request.path):
        return {}
    chat = request.COOKIES.get('chatid')
    admin = AdminBot.objects.get(tgid=chat)
    context = get_context(request, admin)
    alerts = get_alerts(admin)
    return context | alerts


def get_context(request, admin):
    context = {
        'first_name': admin.first_name,
        'last_name': admin.last_name,
        'tgid': admin.tgid
    }
    if botid := request.resolver_match.kwargs.get('botid'):
        bot = Bot.objects.get(id=botid)
        context['botid'] = botid
        context['bot_name'] = bot.name
        context['bot_login'] = bot.login[1:]
        context['is_active'] = bot.is_active
        context['is_paid'] = bot.is_paid
        context['days'] = bot.get_days_display
        context['hours'] = bot.hours
        context['tz'] = bot.tz
    return context


def get_alerts(admin):
    bots = Bot.objects.filter(admin__tgid=admin.tgid)
    if not bots:
        return {}
    newuser = alerts_newuser(bots)
    endtask = alerts_endtask(bots)
    endtarif = alerts_endtarif(bots)
    return newuser | endtask | endtarif


def alerts_newuser(bots):
    alerts_newuser = 0
    alerts_count_newuser = []
    for bot in bots:
        cur_count = bot.student_set.filter(
            studentbot__is_activated=False).count()
        if cur_count > 0:
            alerts_newuser += cur_count
            alerts_count_newuser.append((bot.id, bot.name, cur_count))
    return {
        'alerts_count_newuser': alerts_count_newuser,
        'alerts_newuser': alerts_newuser,
    }


def alerts_endtask(bots):
    alerts_count_endtask = {}
    cat_names = {}
    bots = bots.prefetch_related('task')
    for bot in bots:
        tasks = bot.task.filter(time__isnull=True)
        categories = {}
        cat_names = {}
        for task in tasks:
            if categories.get(task.category.id):
                categories[task.category.id] += 1
            else:
                categories[task.category.id] = 1
                cat_names[task.category.id] = task.category.name
        alert = False
        temp_cat = dict(categories)
        for category, count in categories.items():
            if count < settings.ALERT_MIN_TASKS:
                alert = True
            else:
                temp_cat.pop(category, None)
                cat_names.pop(category, None)
        if alert:
            alerts_count_endtask[bot.id] = temp_cat
    return {
        'alerts_count_endtask': alerts_count_endtask,
        'cat_names': cat_names,
    }


def alerts_endtarif(bots):
    alerts_tarif = []
    bots = bots.select_related('tarif')
    for bot in bots:
        now = datetime.now(pytz.timezone(bot.tz))
        end_tarif = bot.end_time
        if now + timedelta(days=3) > end_tarif:
            alerts_tarif.append(bot.name)
    return {
        'alerts_tarif': alerts_tarif,
    }
