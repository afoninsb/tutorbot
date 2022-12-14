from datetime import datetime, timedelta

from bots.models import Bot
from content.models import Category, Log, Task
from stats.models import Rating


def rating(tokens: list, now):
    now = datetime(now.year, now.month, now.day)
    yesterday = (now - timedelta(days=1))
    for token in tokens:
        bot = Bot.objects.get(token=token)
        objs = []
        from_log = Log.objects.\
            filter(bot=bot).\
            filter(time__gte=now).\
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


def disable_categories_bots(bots):
    for bot in bots:
        categories = Category.objects.filter(bot=bot).\
            filter(is_active=True)
        for category in categories:
            if not Task.objects.filter(category=category).\
                    filter(time__isnull=True).exists():
                category.update(is_active=False)
        if not Category.objects.filter(bot=bot).\
                filter(is_active=True).exists():
            bot.update(is_active=False)
