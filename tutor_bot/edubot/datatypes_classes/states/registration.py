from edubot.main_classes import BotData, UserData
from edubot.keyboards.main import hide_kbrd
from edubot.main_classes.localdata import StudentUser


def reg_start(message: dict, bot: BotData, user: UserData, **kwargs) -> None:
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


def reg_password(message: dict, bot: BotData, user: UserData, **kwargs) -> None:
    """Получили пароль и обрабатываем его.
    Args:
        message (dict): объект message, полученный с вебхука.
    """
    if message.get('text') and user.is_right_bot_password(bot, message.get('text')):
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


def reg_first_name(message: dict, bot: BotData, user: UserData, **kwargs) -> None:
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


def reg_last_name(message: dict, bot: BotData, user: UserData, **kwargs) -> None:
    """Получили Фамилию и обрабатываем её. Завершаем регистрацию.
    Args:
        message (dict): объект message, полученный с вебхука.
    """
    if message.get('text'):
        user.edit(last_name=message['text'], state='')
        cur_temp_user = user.get_info
        text = f'''
        Отлично, {cur_temp_user.last_name} {cur_temp_user.first_name}!
        Теперь дождитесь, пока учитель вас одобрит для работы с ботом'''
        student_user = StudentUser(user.chat_id, bot.token)
        student_user.to_base(
            tgid=user.chat_id,
            first_name=cur_temp_user.first_name,
            last_name=cur_temp_user.last_name,
        )
        student_user.to_bot
    else:
        text = 'Шаг 3. Введите вашу Фамилию (только Фамилию):'
    answer = {
        'chat_id': user.chat_id,
        'text': text,
        'reply_markup': hide_kbrd(),
    }
    bot.send_answer(answer)
