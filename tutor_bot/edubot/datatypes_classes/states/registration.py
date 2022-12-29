from typing import Any, Dict
from edubot.keyboards.main import hide_kbrd
from core.main_classes import BotData, StudentUser, TempUser, UserData


def reg_start(
        message: Dict[str, Any], bot: BotData, user: UserData, **kwargs
) -> None:
    """Старт процедуры регистрации."""
    text = '''
    Добрый день!
    Вы беседуете с ботом платформы образовательных ботов StudyBot.Fun.
    Чтобы начать работать с платформой, необходимо зарегистрироваться.
    Всего 3 простых шага.

    Шаг 1. Введите пароль, выданный Вам учителем:'''
    answer = {
        'chat_id': user.chat_id,
        'text': text,
        'reply_markup': hide_kbrd(),
    }
    user.edit(state='password')
    bot.send_answer(answer)


def reg_password(
        message: Dict[str, Any], bot: BotData, user: UserData, **kwargs
) -> None:
    """Получили пароль и обрабатываем его.

    Args:
        message (dict): объект message, полученный с вебхука.
    """
    if (
        message.get('text')
        and user.is_right_bot_password(bot, message.get('text'))
    ):
        text = '''Отлично!

        Шаг 2. Введите ваше Имя (только Имя):'''
        user.edit(state='first_name')
    else:
        text = 'Шаг 1. Введите пароль, выданный Вам учителем:'
    answer = {
        'chat_id': user.chat_id,
        'text': text,
        'reply_markup': hide_kbrd(),
    }
    bot.send_answer(answer)


def reg_first_name(
        message: Dict[str, Any], bot: BotData, user: UserData, **kwargs
) -> None:
    """Получили Имя и обрабатываем его.

    Args:
        message (dict): объект message, полученный с вебхука.
    """
    if message.get('text'):
        text = f'''
        Отлично, {message['text']}!

        Шаг 3. Введите вашу Фамилию (только Фамилию):'''
        user.edit(first_name=message['text'], state='last_name')
    else:
        text = 'Шаг 2. Введите ваше Имя (только Имя):'
    answer = {
        'chat_id': user.chat_id,
        'text': text,
        'reply_markup': hide_kbrd(),
    }
    bot.send_answer(answer)


def reg_last_name(
        message: Dict[str, Any], bot: BotData, user: UserData, **kwargs
) -> None:
    """Получили Фамилию и обрабатываем её. Завершаем регистрацию.

    Args:
        message (dict): объект message, полученный с вебхука.
    """
    if message.get('text'):
        text = end_registration(user, message, bot)
    else:
        text = 'Шаг 3. Введите вашу Фамилию (только Фамилию):'
    answer = {
        'chat_id': user.chat_id,
        'text': text,
        'reply_markup': hide_kbrd(),
    }
    bot.send_answer(answer)


def end_registration(
    user: UserData, message: Dict[str, Any], bot: BotData
) -> str:
    user.edit(last_name=message['text'], state='')
    result = f'''
        Отлично, {message['text']} {user.firstname}!
        Теперь дождитесь, пока учитель вас одобрит для работы с ботом'''
    student_user = StudentUser(user.chat_id, bot.token)
    student_user.to_base(
        tgid=user.chat_id,
        first_name=user.firstname,
        last_name=message['text'],
    )
    student_user.to_bot
    temp_user = TempUser(user.chat_id)
    temp_user.delete()
    return result
