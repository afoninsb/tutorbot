import pytz
from datetime import datetime, timedelta
from django.conf import settings

from bots.models import Bot
from users.models import AdminBot


def get_admin(request):
    if ('/tgbot_backend' in request.path
            or '/webhook' in request.path
            or '/admin' in request.path
            or 'stats/user/' in request.path
            or '/favicon.ico' in request.path):
        return {}
    chat = request.COOKIES.get('chatid')
    admin = AdminBot.objects.get(tgid=chat)
    return {
        'first_name': admin.first_name,
        'last_name': admin.last_name,
        'tgid': admin.tgid,
    }


def get_bot_id(request):
    try:
        data = request.resolver_match.kwargs
    except Exception:
        return {}
    return {'bot_id': data['botid'], } if 'botid' in data else {}


def get_bot(request):
    if data := get_bot_id(request):
        bot = Bot.objects.get(id=data['bot_id'])
        return {
            'botid': bot.id,
            'bot_name': bot.name,
            'bot_login': bot.login[1:],
            'is_active': bot.is_active,
            'days': bot.get_days_display,
            'hours': bot.hours,
            'tz': bot.tz,
        }
    return {}


def alerts_newuser(request):
    if ('/tgbot_backend' in request.path
            or '/webhook' in request.path
            or '/admin' in request.path
            or 'stats/user/' in request.path):
        return {}
    alerts_newuser = 0
    alerts_count_newuser = []
    admin = get_admin(request)
    bots = Bot.objects.filter(
        admin__tgid=admin['tgid'])
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


def alerts_endtask(request):
    if ('/tgbot_backend' in request.path
            or '/webhook' in request.path
            or '/admin' in request.path
            or 'stats/user/' in request.path):
        return {}
    alerts_count_endtask = {}
    cat_names = {}
    admin = get_admin(request)
    bots = Bot.objects.filter(
        admin__tgid=admin['tgid']).prefetch_related('task')
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


def alerts_endtarif(request):
    if ('/tgbot_backend' in request.path
            or '/webhook' in request.path
            or '/admin' in request.path
            or 'stats/user/' in request.path):
        return {}
    alerts_tarif = []
    admin = get_admin(request)
    bots = Bot.objects.filter(
        admin__tgid=admin['tgid']).select_related('tarif')
    for bot in bots:
        now = datetime.now(pytz.timezone(bot.tz))
        end_tarif = bot.end_time
        if now + timedelta(days=3) > end_tarif:
            alerts_tarif.append(bot.name)
    return {
        'alerts_tarif': alerts_tarif,
    }
