def get_task(bot):
    all_tasks = []
    categories = bot.category.filter(is_active=True)
    for category in categories:
        if tasks := category.task.filter(time__isnull=True):
            all_tasks[-1:-1:] = list(tasks)
    return choice(all_tasks)


def get_students_tgids(bot):
    return list(
        bot.student_set.filter(
            studentbot__is_activated=True).values_list('tgid', flat=True)
    )


def send_task(bot_tg):
    from edubot.keyboards.inline import push_answer_kbrd

    cur_bot = get_object_or_404(Bot, token=bot_tg)
    task = get_task(cur_bot)
    message_text = {
        'text': f'<b>Задание № {task.id}</b>\n\n{task.text}',
        'parse_mode': 'HTML'
    }
    if task.img:
        message_img = {
            'photo': f'{settings.BASE_URL}{settings.MEDIA_URL}{task.img}',
        }
    message_button = {
        'text': 'Для ответа нажмите на кнопку:',
        'reply_markup': push_answer_kbrd(task.id),
    }

    users_tgids = get_students_tgids(cur_bot)

    bot = BotData(bot_tg)

    for user_tgid in users_tgids:

        message_text['chat_id'] = user_tgid
        bot.send_answer(message_text)

        if task.img:
            message_img['chat_id'] = user_tgid
            bot.send_photo(message_img)

        message_button['chat_id'] = user_tgid
        bot.send_answer(message_button)

        sleep(0.5)

    Task.objects.filter(id=task.id).update(
        time=datetime.now(pytz.timezone('UTC')))


if __name__ == '__main__':
    import os
    import sys
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    from tutor_bot import asgi
    import django
    django.setup()

    import pytz
    from datetime import datetime
    from django.conf import settings
    from django.shortcuts import get_object_or_404
    from random import choice
    from time import sleep

    from edubot.main_classes import BotData
    from bots.models import Bot
    from content.models import Task

    send_task(sys.argv[1])
    sys.exit(0)
