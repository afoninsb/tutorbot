def cron_task():
    import pytz
    import subprocess
    from datetime import datetime
    from bots.models import Bot
    from buildrating import rating

    bots = Bot.objects.filter(is_active=True)
    tokens_tasks = []
    tokens_rating = []
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
        if hour == '3':
            tokens_rating.append(bot.token)

    if tokens_tasks:
        len_tokens_tasks = len(tokens_tasks)
        proc = [1]*len_tokens_tasks
        for count, token in enumerate(tokens_tasks):
            proc[count] = subprocess.Popen(
                ['./venv/bin/python', 'tutor_bot/cron/sendtask.py', token]
            )
        for i in range(len_tokens_tasks):
            stdout_byte, stderr_byte = proc[i].communicate()
    if tokens_rating:
        rating(tokens_rating, now)


if __name__ == '__main__':
    import os
    import sys
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    from tutor_bot import asgi
    import django

    django.setup()
    cron_task()