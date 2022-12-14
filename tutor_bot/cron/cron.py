def cron_task():
    import subprocess
    import pytz
    from datetime import datetime

    from bots.models import Bot
    from functions import disable_categories_bots

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
    if tokens_tasks:
        len_tokens_tasks = len(tokens_tasks)
        proc = [1]*len_tokens_tasks
        for count, token in enumerate(tokens_tasks):
            proc[count] = subprocess.Popen(
                [
                    '/home/a/afoninry/tutor.studybot.fun/venv_django/bin/python3',
                    '/home/a/afoninry/tutor.studybot.fun/tutor_bot/cron/sendtask.py',
                    token
                ]
            )
        for i in range(len_tokens_tasks):
            stdout_byte, stderr_byte = proc[i].communicate()

    disable_categories_bots(bots)


def cron_rating():
    import pytz
    from datetime import datetime

    from bots.models import Bot
    from functions import rating

    bots = Bot.objects.all()
    tokens_rating = []
    for bot in bots:
        now = datetime.now(pytz.timezone(bot.tz))
        hour = str(now.hour)
        if hour == '3':
            tokens_rating.append(bot.token)
    if tokens_rating:
        rating(tokens_rating, now)


if __name__ == '__main__':
    import os
    import sys
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    import django

    from tutor_bot import asgi

    django.setup()
    cron_task()
    cron_rating()
