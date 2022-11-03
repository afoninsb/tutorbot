from edubot.main_classes import BotData, LocalData


def change_first_name(message: dict, bot: BotData, local: LocalData) -> None:
    """Редактирование имени юзера.
    Args:
        message (dict): объект message, полученный с вебхука.
    """
    if message.get('text'):
        text = f'''
        Хорошо, {message['text']}!
        Теперь ведите вашу Фамилию (только Фамилию):'''
        local.user_edit(first_name=message['text'], state='change_last_name')
    else:
        text = 'Введите ваше Имя (только Имя):'
    answer = {
        'chat_id': local.chat_id,
        'text': text,
    }
    bot.send_answer(answer)


def change_last_name(message: dict, bot: BotData, local: LocalData) -> None:
    """Редактирование фамилии юзера.
    Args:
        message (dict): объект message, полученный с вебхука.
    """
    if message.get('text'):
        text = f'Итак, теперь вы - {local.user_first_name} {message["text"]}!'
        local.user_edit(last_name=message['text'], state='')
    else:
        text = 'Введите вашу Фамилию (только Фамилию):'
    answer = {
        'chat_id': local.chat_id,
        'text': text,
    }
    bot.send_answer(answer)
