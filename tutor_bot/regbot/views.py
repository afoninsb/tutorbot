import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from edubot.main_classes import BotData
from edubot.main_classes.localdata import AdminUser, TempUser

from .datatypes_classes import (HighLevelCallback, HighLevelCommand,
                                HighLevelState, HighLevelText, Road)


@csrf_exempt
def webhook(request, bot_tg):

    # Получаем словарь из тела полученного вебхука
    try:
        from_tg = json.loads(request.body)
    except Exception:
        from_tg = {}

    # Создаём объект BotData для работы с данными с вебхука
    bot = BotData(bot_tg)
    tgid = bot.user_id(from_tg)

    # Создаём объект LocalData для работы с базой данных
    user = AdminUser(tgid)
    is_admin = True

    # Если юзера нет в базе, добавляем в базу и запускаем регистрацию
    if not user.is_in_base:
        is_admin = False
        user = TempUser(tgid)
        user.to_base(
            tgid=tgid,
            first_name='fn',
            last_name='ln',
            org='org',
            position='pos',
            why='why',
            state='start'
        )

    # Получаем объект message
    message = bot.get_message(from_tg)

    # Получаем тип обновления
    data_type = bot.get_data_type(from_tg)

    # Если у юзера есть состояние, в тип обонвления помещаем его,
    # Команды имеют приоритет - рассматриваются первыми
    cur_user = user.get_info
    if (
        message['text'] == '/start'
        or cur_user.state
        and data_type != 'command'
    ):
        data_type = 'state'
    # Создаём объект Road, определяющий направление движения
    road = Road()

    # Набор возможных направлений движения
    pathes = (
        HighLevelCommand(),
        HighLevelState(),
        HighLevelCallback(),
        HighLevelText()
    )

    # Добавляем направления к нашему объекту Road
    for path in pathes:
        road.attach(path)

    # Запускаем движения по выбранному направлению,
    # определяемому параметром data_type
    road.go(data_type, bot, user, message=message,
            from_tg=from_tg, cur_user=cur_user, is_admin=is_admin)

    return render(request, 'webhook/123.html')
