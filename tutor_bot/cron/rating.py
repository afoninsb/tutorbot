"""Выполнение заданий, повторяемых регулярно."""


def cron_rating():
    """Обновление рейтинга."""
    import pytz
    from datetime import datetime

    from bots.models import Bot
    from functions import rating

    bots = Bot.objects.all()
    tokens_rating = []
    for bot in bots:
        now = datetime.now(pytz.timezone(bot.tz))
        today = datetime(now.year, now.month, now.day)
        if str(bot.last_rating) < str(today):
        # hour = str(now.hour)
        # if hour in {'2', '8', '14', 20', '02', '08'}:
            tokens_rating.append((bot.token, today))
    if tokens_rating:

        # Если есть боты для обновления, обновляем
        rating(tokens_rating)


if __name__ == '__main__':
    import os
    import sys
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    import django

    from tutor_bot import asgi

    django.setup()
    cron_rating()
