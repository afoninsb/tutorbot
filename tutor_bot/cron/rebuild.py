def rating(tokens):
    """Обновляем рейтинг."""
    from datetime import datetime, timedelta

    from bots.models import Bot
    from content.models import Log
    from stats.models import Rating

    for token in tokens:
        bot = Bot.objects.get(id=token)
        for plus_day in range(68):
            today = (datetime(2023, 1, 13) + timedelta(days=plus_day))
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


if __name__ == '__main__':
    import os
    import sys
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    import django

    from tutor_bot import asgi

    django.setup()
    rating((1900288220,))
