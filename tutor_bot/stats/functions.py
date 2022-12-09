import contextlib


def compare_logs(stats, logs, id, start):
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


def get_stats(array, dates, student):
    stats = {}
    for element in array:
        stats[element.id] = [0, 0, 0]
        if logs := element.log.all():
            if student:
                logs = logs.filter(student=student)
            if dates:
                logs = logs.filter(
                    time__gte=dates[0],
                    time__lte=dates[1],
                )
            stats[element.id][0] = logs.count()
            compare_logs(stats, logs, element.id, -1)
    return stats


def create_rating():
    pass
