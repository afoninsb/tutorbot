from edubot.main_classes import BotData
from edubot.main_classes.localdata import UserData


def change_first_name(
        message: dict, bot: BotData, user: UserData, **kwargs
) -> None:
    """Редактирование имени юзера.
    Args:
        message (dict): объект message, полученный с вебхука.
    """
    if message.get('text'):
        text = f'''
        Хорошо, {message['text']}!
        Теперь ведите вашу Фамилию (только Фамилию):'''
        user.edit(first_name=message['text'], state='change_last_name')
    else:
        text = 'Введите ваше Имя (только Имя):'
    answer = {
        'chat_id': user.chat_id,
        'text': text,
    }
    bot.send_answer(answer)


def change_last_name(
        message: dict, bot: BotData, user: UserData, **kwargs
) -> None:
    """Редактирование фамилии юзера.
    Args:
        message (dict): объект message, полученный с вебхука.
    """
    if message.get('text'):
        user.edit(last_name=message['text'], state='')
        text = f'Итак, теперь вы - {user.full_name} {message["text"]}!'
    else:
        text = 'Введите вашу Фамилию (только Фамилию):'
    answer = {
        'chat_id': user.chat_id,
        'text': text,
    }
    bot.send_answer(answer)
