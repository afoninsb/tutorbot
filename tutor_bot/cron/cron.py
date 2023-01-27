"""Выполнение заданий, повторяемых регулярно."""

from types import ModuleType
from typing import List
from django.conf import LazySettings


def cron_task():
    """Главная функция cron."""
    import os
    import pytz
    import subprocess
    from datetime import datetime
    from django.conf import settings

    from bots.models import Bot

    bots = Bot.objects.filter(is_active=True)
    if not bots:
        return

    tokens_tasks = []
    for bot in bots:
        now = datetime.now(pytz.timezone(bot.tz))
        hour = str(now.hour)
        week_day = now.weekday()
        bot_hours = bot.hours.split()
        if (
            (bot.days == Bot.DayType.WEEK_DAYS
             or bot.days == Bot.DayType.WORKING_DAYS and week_day < 5)
            and hour in bot_hours
        ):
            tokens_tasks.append(bot.token)

    # Если есть боты для рассылки заданий, рассылаем.
    if tokens_tasks:
        send_task(os, settings, tokens_tasks, subprocess)


def send_task(
        os: ModuleType,
        settings: LazySettings,
        tokens_tasks: List[str],
        subprocess: ModuleType
):
    if settings.DEBUG:
        path_python = os.path.join(
            settings.BASE_DIR.parent, 'venv', 'bin', 'python3'
        )
    else:
        path_python = os.path.join(
            settings.BASE_DIR.parent, 'venv_django', 'bin', 'python3'
        )
    path_script = os.path.join(
        settings.BASE_DIR, 'cron', 'sendtask.py'
    )
    len_tokens_tasks = len(tokens_tasks)
    proc = [1]*len_tokens_tasks
    for count, token in enumerate(tokens_tasks):
        proc[count] = subprocess.Popen([path_python, path_script, token])
    for i in range(len_tokens_tasks):
        stdout_byte, stderr_byte = proc[i].communicate()


if __name__ == '__main__':
    import os
    import sys
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    import django

    from tutor_bot import asgi

    django.setup()
    cron_task()
