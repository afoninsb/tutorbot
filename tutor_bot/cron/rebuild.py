from datetime import timedelta
import datetime

import pytz

from bots.models import Bot
from content.models import Log
from stats.models import Rating


def rating(tokens):
    """Обновляем рейтинг."""
    for token in tokens:
        bot = Bot.objects.get(token=token)
        now = datetime.now(pytz.timezone(bot.tz))
        today = datetime(now.year, now.month, now.day)
        yesterday = (today - timedelta(days=1))
        objs = []
        from_log = Log.objects.\
            filter(bot=bot).\
            filter(time__gte=yesterday, time__lt=today).\
            select_related('student')
        log_scores = {}
        for log in from_log:
            if log.student in log_scores:
                log_scores[log.student] += log.score
            else:
                log_scores[log.student] = log.score
        from_rating = Rating.objects.\
            filter(bot=bot).\
            filter(time=yesterday).\
            select_related('student')
        for rating in from_rating:
            scores = rating.score
            if rating.student in log_scores:
                scores += log_scores[rating.student]
                del log_scores[rating.student]
            objs.append(
                Rating(
                    bot=bot,
                    student=rating.student,
                    score=scores,
                    time=today
                )
            )
        if log_scores:
            objs.extend(Rating(
                bot=bot,
                student=student,
                score=score,
                time=today
            )
                for student, score in log_scores.items())

        Rating.objects.bulk_create(objs)
