import json

from django.conf import settings


def push_answer_kbrd(task_id: int) -> json:
    """Кнопка Ответить на вопрос.

    Args:
        task_id (int): id задания.
    Returns:
        json: Клавиатура в формате json.
    """
    inline_button = [{
        'text': 'Ответить',
        'callback_data': f'answer:{task_id}'
    }]
    kkbd = {'inline_keyboard': [inline_button]}
    return json.dumps(kkbd)


def reply_kbrd(chat_id: int) -> json:
    """Кнопка Ответить при переписке.

    Args:
        chat_id (int): Telegram chat_id юзера.
    Returns:
        json: Клавиатура в формате json.
    """
    inline_button = [{
        'text': 'Ответить',
        'callback_data': f'reply:{chat_id}'
    }]
    rkbd = {'inline_keyboard': [inline_button]}
    return json.dumps(rkbd)


def admin_kbrd(chat_id: int, pin: str) -> json:
    """Кнопка Войти в административную панель.

    Args:
        chat_id (int): Telegram chat_id юзера.
        pin (str): pin-код для входа в админпанель.
    Returns:
        json: Клавиатура в формате json.
    """
    inline_button = [{
        'text': 'Войти в административную панель',
        'url': f"{settings.BASE_URL}/login/enter/{chat_id}/{pin}/"
    }]
    akbd = {'inline_keyboard': [inline_button]}
    return json.dumps(akbd)


def userstat_kbr(bot_id, user_id: int, pin: str) -> json:
    """Кнопка Моя статистика.

    Args:
        user_id (int): id юзера.
        pin (str): pin-код для входа в статистику.
    Returns:
        json: Клавиатура в формате json.
    """
    inline_button = [{
        'text': 'Смотреть статистику',
        'url': f"{settings.BASE_URL}/bot/{bot_id}/stats/user/{user_id}/{pin}/"
    }]
    akbd = {'inline_keyboard': [inline_button]}
    return json.dumps(akbd)
