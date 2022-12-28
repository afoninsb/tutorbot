import contextlib
from typing import Dict, List, Tuple, Union
from django.db.models.query import QuerySet

from users.models import Student


def compare_logs(
        stats: Dict[int, List[int]],
        logs: QuerySet,
        id: int,
        start: int
) -> Dict[int, List[int]]:
    """Получение и обработка данных из логов."""
    for log in logs:
        if start == 0:
            stats[id][1] += 1
        if log.is_truth:
            stats[id][start+2] += 1
    with contextlib.suppress(ZeroDivisionError):
        stats[id][start+3] = (
            stats[id][start+2] / stats[id][start+1]
        )
        stats[id][start+3] = int(float(
            format(stats[id][start+3], ".2f")
        ) * 100)
    return stats


def get_stats(
        array: QuerySet,
        dates: Tuple[str, str],
        student: Union[None, Student],
        cat_id: int
) -> Dict[int, List[int]]:
    """Построение статистики в категории за указанный период."""
    stats = {}
    for element in array:
        stats[element.id] = [0, 0, 0]
        if logs := element.log.all():
            if student:
                logs = logs.filter(student=student)
            else:
                logs = logs.filter(category__id=cat_id)
            if dates:
                logs = logs.filter(
                    time__gte=dates[0],
                    time__lte=dates[1],
                )
            stats[element.id][0] = logs.count()
            compare_logs(stats, logs, element.id, -1)
    return stats
