from edubot.main_classes import BotData, LocalData


def reg_start(message: dict, bot: BotData, local: LocalData) -> None:
    """Старт процедуры регистрации."""
    text = '''
    Добрый день!
    Вы беседуете с ботом платформы образовательных ботов StudyBot.Fun.
    Чтобы начать работать с платформой, необходимо зарегистрироваться.
    Всего 3 простых шага.

    Шаг 1. Введите пароль, выданный Вам учителем:'''
    answer = {
        'chat_id': local.chat_id,
        'text': text,
    }
    local.user_edit(state='password')
    bot.send_answer(answer)


def reg_password(message: dict, bot: BotData, local: LocalData) -> None:
    """Получили пароль и обрабатываем его.
    Args:
        message (dict): объект message, полученный с вебхука.
    """
    if message.get('text') and message.get('text') == local.bot_password:
        # Если новый ученик на платформе, регистрируем
        if local.user_full_name == 'fn ln':
            text = '''Отлично!

            Шаг 2. Введите ваше Имя (только Имя):'''
            local.user_edit(state='first_name')
        # Если уже работал с другим ботом, регистрацию пропускаем
        else:
            local.user_to_bot
            text = 'Отлично! Продолжайте работать.'
            local.user_edit(state='')
    else:
        text = 'Шаг 1. Введите пароль, выданный Вам учителем:'
    answer = {
        'chat_id': local.chat_id,
        'text': text,
    }
    bot.send_answer(answer)


def reg_first_name(message: dict, bot: BotData, local: LocalData) -> None:
    """Получили Имя и обрабатываем его.
    Args:
        message (dict): объект message, полученный с вебхука.
    """
    if message.get('text'):
        text = f'''
        Отлично, {message['text']}!

        Шаг 3. Введите вашу Фамилию (только Фамилию):'''
        local.user_edit(first_name=message['text'], state='last_name')
    else:
        text = 'Шаг 2. Введите ваше Имя (только Имя):'
    answer = {
        'chat_id': local.chat_id,
        'text': text,
    }
    bot.send_answer(answer)


def reg_last_name(message: dict, bot: BotData, local: LocalData) -> None:
    """Получили Фамилию и обрабатываем её. Завершаем регистрацию.
    Args:
        message (dict): объект message, полученный с вебхука.
    """
    if message.get('text'):
        text = f'''
        Отлично, {local.user_first_name} {message['text']}!

        Теперь Вам необходимо <b>присоединиться к группе</b>.
        Для этого:
            либо 1. Отправьте команду /signup_to_group
        и введите пин-код, выданный учителем;
            либо 2. Дождитесь, пока учитель Вас добавит в группу сам.'''
        local.user_edit(last_name=message['text'], state='')
        local.user_to_bot
    else:
        text = 'Шаг 3. Введите вашу Фамилию (только Фамилию):'
    answer = {
        'chat_id': local.chat_id,
        'text': text,
        'parse_mode': 'HTML',
    }
    bot.send_answer(answer)
