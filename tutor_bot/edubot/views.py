import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .datatypes_classes import (HighLevelCallback, HighLevelCommand,
                                HighLevelState, HighLevelText, Road)
from .main_classes import BotData, LocalData


@csrf_exempt
def webhook(request, bot_tg):

    # Получаем словарь из тела полученного вебхука
    try:
        from_tg = json.loads(request.body)
    except Exception:
        from_tg = {}

    # Создаём объект BotData для работы с данными с вебхука
    bot = BotData(bot_tg)

    # Создаём объект LocalData для работы с базой данных
    local = LocalData(bot_tg, bot.user_id(from_tg))

    # Если юзера нет в базе, добавляем в базу и запускаем регистрацию
    if not local.user_is_in_base:
        local.user_new

    # Если юзер в базе, но не в этом боте, посылаем на пароль
    elif not local.user_is_in_bot:
        local.user_edit(state='start')

    # Получаем объект message
    message = bot.get_message(from_tg)

    # Получаем тип обновления
    data_type = bot.get_data_type(from_tg)

    # Если у юзера есть состояние, в тип обонвления помещаем его,
    # Команды имеют приоритет - рассматриваются первыми
    if local.user_state and data_type != 'command':
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
    road.go(data_type, bot, local, message=message, from_tg=from_tg)

    return render(request, 'webhook/123.html')
