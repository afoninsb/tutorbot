from datetime import timedelta
from django.db.models.query import QuerySet

from bots.models import Bot
from content.models import Category, Log, Task
from stats.models import Rating


def rating(tokens):
    """Обновляем рейтинг."""
    for data in tokens:
        token = data[0]
        today = data[1]
        yesterday = (today - timedelta(days=1))
        bot = Bot.objects.get(token=token)
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

        Bot.objects.filter(token=token).update(last_rating=today)


def disable_categories_bots(bots: QuerySet):
    """Останавливаем категории бота."""
    objs_bot = []
    for bot in bots:
        if categories := Category.objects.\
                filter(bot=bot).filter(is_active=True):
            objs_cat = []
            for category in categories:
                if Task.objects.filter(category=category).\
                        filter(time__isnull=True).exists():
                    continue
                category.is_active = False
                objs_cat.append(category)
            if objs_cat:
                Category.objects.bulk_update(objs_cat, ['is_active'])
        if Category.objects.filter(bot=bot).\
                filter(is_active=True).exists():
            continue
        bot.is_active = False
        objs_bot.append(bot)
    if objs_bot:
        Bot.objects.bulk_update(objs_bot, ['is_active'])
