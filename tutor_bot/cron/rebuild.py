from datetime import datetime, timedelta

from bots.models import Bot
from content.models import Log
from stats.models import ReRating


def rating(tokens):
    """Обновляем рейтинг."""
    for token in tokens:
        bot = Bot.objects.get(token=token)
        plus_day = 0
        while plus_day < 35:
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
            from_rating = ReRating.objects.\
                filter(bot=bot).\
                filter(time=yesterday).\
                select_related('student')
            for rating in from_rating:
                scores = rating.score
                if rating.student in log_scores:
                    scores += log_scores[rating.student]
                    del log_scores[rating.student]
                objs.append(
                    ReRating(
                        bot=bot,
                        student=rating.student,
                        score=scores,
                        time=today
                    )
                )
            if log_scores:
                objs.extend(ReRating(
                    bot=bot,
                    student=student,
                    score=score,
                    time=today
                )
                    for student, score in log_scores.items())

            ReRating.objects.bulk_create(objs)

            plus_day += 1


if __name__ == '__main__':
    rating((5529264374, 5653938367))
