import json

from django.conf import settings


def approve_admin(chat_id: int) -> str:
    """Клавиатура Одобрить/Отклонить для заявки в даины.

    Args:
        chat_id (int): Telegram chat_id юзера.
    Returns:
        str: Клавиатура в формате json.
    """
    akbd = {}
    keyboard = []
    inline_button = [
        {
            'text': 'Одобрить',
            'callback_data': f'approve:{chat_id}'
        },
        {
            'text': 'Отклонить',
            'callback_data': f'reject:{chat_id}'
        }
    ]
    keyboard.append(inline_button)
    akbd['inline_keyboard'] = keyboard
    return json.dumps(akbd)


def reply_kbrd(chat_id: int) -> str:
    """Кнопка Ответить при переписке.

    Args:
        chat_id (int): Telegram chat_id юзера.
    Returns:
        str: Клавиатура в формате json.
    """
    rkbd = {}
    keyboard = []
    inline_button = [{
        'text': 'Ответить',
        'callback_data': f'reply:{chat_id}'
    }]
    keyboard.append(inline_button)
    rkbd['inline_keyboard'] = keyboard
    return json.dumps(rkbd)


def admin_kbrd(chat_id: int, pin: str) -> str:
    """Кнопка Войти в административную панель.

    Args:
        chat_id (int): Telegram chat_id юзера.
        pin (str): pin-код для входа в админпанель.
    Returns:
        str: Клавиатура в формате json.
    """
    akbd = {}
    keyboard = []
    inline_button = [{
        'text': 'Войти в административную панель',
        'url': f"{settings.BASE_URL}/login/enter/{chat_id}/{pin}/"
    }]
    keyboard.append(inline_button)
    akbd['inline_keyboard'] = keyboard
    return json.dumps(akbd)
