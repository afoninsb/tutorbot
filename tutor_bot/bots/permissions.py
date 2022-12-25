import pytz
from datetime import datetime
from django.conf import settings
from django.shortcuts import get_object_or_404

from bots.models import Bot
from tarifs.models import Tarif
from users.models import StudentBot


def can_bot_run(bot):
    permission = (1,)

    num_students = StudentBot.objects.filter(bot=bot).count()
    if (
        num_students > settings.STUDENT_FREE_TARIF
        and bot.tarif != Tarif.objects.filter(
            duration=Tarif.TarifsTypes.FREE)[0]
    ):
        permission = (
            5,
            'Нельзя запустить бота. Необходимо оплатить тариф!',
            'tarifs:index'
        )

    if not (bot.days and bot.hours):
        permission = (
            4,
            'Нельзя запустить бота. Необходимо настроить расписание!',
            'bots:bot_schedule'
        )

    if not bot.category.filter(is_active=True).exists():
        permission = (
            3,
            ('Нельзя запустить бота. Необходимо включить '
             'хотя бы одну категорию!'),
            'content:category'
        )

    now = datetime.now(pytz.timezone(bot.tz))
    if now >= bot.end_time:
        permission = (
            2,
            'Нельзя запустить бота. Необходимо продлить тариф!',
            'tarifs:index'
        )

    return permission


def stop_bot(botid):
    cur_bot = get_object_or_404(Bot, id=botid)
    if not cur_bot.is_active:
        return
    num_students = StudentBot.objects.filter(bot=cur_bot).count()
    now = datetime.now(pytz.timezone(cur_bot.tz))
    if (
        num_students > settings.STUDENT_FREE_TARIF
        and cur_bot.tarif != Tarif.objects.filter(
            duration=Tarif.TarifsTypes.FREE)[0]
        or now >= cur_bot.end_time
    ):
        Bot.objects.filter(id=cur_bot.id).\
            update(is_active=False, is_paid=False)
