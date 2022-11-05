def cron_task():
    import pytz
    import subprocess
    from datetime import datetime
    from bots.models import Bot
    now = datetime.now(pytz.timezone('Europe/Moscow'))
    hour = str(now.hour)
    week_day = now.weekday()
    bots = Bot.objects.filter(is_active=True)
    tokens = []
    for bot in bots:
        bot_hours = bot.hours.split()
        if (
            (bot.days == Bot.DayType.WEEK_DAYS
             or bot.days == Bot.DayType.WORKING_DAYS and week_day < 5)
            and hour in bot_hours
        ):
            tokens.append(bot.token)

    proc = [1]*len(tokens)
    for count, token in enumerate(tokens):
        proc[count] = subprocess.Popen(
            ['./venv/bin/python', 'tutor_bot/cron/sendtask.py', token]
        )
    for i in range(len(tokens)):
        stdout_byte, stderr_byte = proc[i].communicate()


if __name__ == '__main__':
    import os
    import sys
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    from tutor_bot import asgi
    import django
    django.setup()
    cron_task()
