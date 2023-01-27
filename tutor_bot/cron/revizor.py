"""Выполнение заданий, повторяемых регулярно."""

from types import ModuleType
from typing import List
from django.conf import LazySettings


def cron_task():
    """Главная функция cron."""
    from bots.models import Bot
    from bots.permissions import stop_bot
    from functions import disable_categories_bots

    bots = Bot.objects.filter(is_active=True)
    if not bots:
        return

    for bot in bots:
        # Надо ли остановить бота?
        stop_bot(bot.id)

    # Может надо остановить отдельные категории в каких-то ботах?
    disable_categories_bots(bots)


if __name__ == '__main__':
    import os
    import sys
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    import django

    from tutor_bot import asgi

    django.setup()
    cron_task()
