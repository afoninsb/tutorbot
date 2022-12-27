from django.conf import settings
from typing import Any, Dict

from edubot.main_classes import BotData
from edubot.main_classes.localdata import UserData
from regbot.keyboards import hide_kbrd
from regbot.keyboards.inline import approve_admin


def reg_start(message: Dict[str, Any], bot: BotData, user: UserData) -> None:
    """Старт процедуры регистрации."""
    text = '''
    Добрый день!
    Вы беседуете с ботом платформы образовательных ботов StudyBot.Fun.
    Для отправки заявки надо пройти 5 простых шагов.

    Шаг 1. Введите Ваше имя (только Имя):'''
    answer = {
        'chat_id': user.chat_id,
        'text': text,
        'reply_markup': hide_kbrd()
    }
    user.edit(state='get_admin_first_name')
    bot.send_answer(answer)


def reg_first_name(
        message: Dict[str, Any], bot: BotData, user: UserData
) -> None:
    """Получили Имя и обрабатываем его."""
    if message.get('text'):
        text = f'''
        Отлично, {message['text']}!

        Шаг 2. Введите вашу Фамилию (только Фамилию):'''
        user.edit(first_name=message['text'], state='get_admin_last_name')
    else:
        text = 'Шаг 1. Введите Ваше имя (только Имя):'
    answer = {
        'chat_id': user.chat_id,
        'text': text,
        'reply_markup': hide_kbrd()
    }
    bot.send_answer(answer)


def reg_last_name(
        message: Dict[str, Any], bot: BotData, user: UserData
) -> None:
    """Получили Фамилию и обрабатываем её. Завершаем регистрацию."""
    if message.get('text'):
        user.edit(last_name=message['text'], state='get_admin_org')
        text = f'''Отлично, {user.full_name}!

        Шаг 3. Ведите организацию, в которой вы работаете:'''
    else:
        text = 'Шаг 2. Введите вашу Фамилию (только Фамилию):'
    answer = {
        'chat_id': user.chat_id,
        'text': text,
        'reply_markup': hide_kbrd()
    }
    bot.send_answer(answer)


def reg_org(message: Dict[str, Any], bot: BotData, user: UserData) -> None:
    """Получили организацию и обрабатываем её. Завершаем регистрацию."""
    if message.get('text'):
        text = '''Ещё немного :)

            Шаг 4. Введите вашу должность:'''
        user.edit(org=message['text'], state='get_admin_position')
    else:
        text = 'Шаг 3. Ведите организацию, в которой вы работаете:'
    answer = {
        'chat_id': user.chat_id,
        'text': text,
        'reply_markup': hide_kbrd()
    }
    bot.send_answer(answer)


def reg_position(
        message: Dict[str, Any], bot: BotData, user: UserData
) -> None:
    """Получили позицию и обрабатываем её. Завершаем регистрацию."""
    if message.get('text'):
        text = '''И последнее....

            Шаг 5. Объясните в 3-х предложениях,
    зачем вам этот бот,
    для чего будете его использовать:'''
        user.edit(position=message['text'], state='get_admin_why')
    else:
        text = 'Шаг 4. Введите вашу должность:'
    answer = {
        'chat_id': user.chat_id,
        'text': text,
        'reply_markup': hide_kbrd()
    }
    bot.send_answer(answer)


def reg_why(message: Dict[str, Any], bot: BotData, user: UserData) -> None:
    """Получили объяснение и обрабатываем его. Завершаем регистрацию."""
    if message.get('text'):
        text = end_registration(message, bot, user)
    else:
        text = '''Объясните в 3-х предложениях, зачем вам этот бот,
        для чего будете его использовать:'''
    answer = {
        'chat_id': user.chat_id,
        'text': text,
        'reply_markup': hide_kbrd()
    }
    bot.send_answer(answer)


def end_registration(
        message: Dict[str, Any], bot: BotData, user: UserData
) -> str:
    """Завершаем регистрацию."""
    user.edit(why=message['text'], state='')
    temp_admin = user.get_info
    text_to_boss = f'''Пришла заявка на нового админа.
            Имя: {temp_admin.first_name}
            Фамилия: {temp_admin.last_name}
            Организация: {temp_admin.org}
            Должность: {temp_admin.position}
            Пояснение: {temp_admin.why}'''
    answer_to_boss = {
        'chat_id': settings.BIG_BOSS_ID,
        'text': text_to_boss,
        'reply_markup': approve_admin(user.chat_id),
    }
    bot.send_answer(answer_to_boss)
    return '''Спасибо за информацию.
            Данные были отправлены супербоссу :)
            После его подтверждения, вы сможете работать на платформе.'''
