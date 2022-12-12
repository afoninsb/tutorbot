from datetime import timedelta

from bots.models import Bot
from content.models import Log
from stats.models import Rating


def rating(tokens: list, now):
    yesterday = (now - timedelta(days=1)).strftime('%Y-%m-%d')
    now = now.strftime('%Y-%m-%d')
    for token in tokens:
        bot = Bot.objects.get(token=token)
        objs = []

        from_log = Log.objects.\
            filter(bot=bot).\
            filter(time__gte=now).\
            filter(is_truth=True).\
            select_related('student')
        log_scores = {log.student: log.score for log in from_log}
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
                    score=scores
                )
            )
        if log_scores:
            objs.extend(Rating(bot=bot, student=student, score=score)
                        for student, score in log_scores.items())

        Rating.objects.bulk_create(objs)
