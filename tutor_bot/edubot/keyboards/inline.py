import json

from django.conf import settings
from django.db.models.query import QuerySet
from edubot.main_classes import LocalData
from edubot.main_classes.localdata import LocalData


def push_kr_kbrd(item: int, kr_out: int, group_id: int) -> json:
    """Кнопка Сдать контрольную работу.
    Args:
        item (int): id темы в тематическом плане.
        kr_out (int): id выдачи контрольной работы.
        group_id (int): id группы.
    Returns:
        json: Клавиатура в формате json.
    """
    kkbd = {}
    keyboard = []
    inline_button = [{
        'text': 'Сдать контрольную работу',
        'callback_data': f'push:k:{item}:{group_id}:{kr_out}'
    }]
    keyboard.append(inline_button)
    kkbd['inline_keyboard'] = keyboard
    return json.dumps(kkbd)


def reply_kbrd(chat_id: int) -> json:
    """Кнопка Ответить при переписке.
    Args:
        chat_id (int): Telegram chat_id юзера.
    Returns:
        json: Клавиатура в формате json.
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


def admin_kbrd(chat_id: int, pin: str) -> json:
    """Кнопка Войти в административную панель.
    Args:
        chat_id (int): Telegram chat_id юзера.
        pin (str): pin-код для входа в админпанель.
    Returns:
        json: Клавиатура в формате json.
    """
    akbd = {}
    keyboard = []
    inline_button = [{
        'text': 'Войти в административную панель',
        'url': f"{settings.BASE_URL}/enter/{chat_id}/{pin}/"
    }]
    keyboard.append(inline_button)
    akbd['inline_keyboard'] = keyboard
    return json.dumps(akbd)


def plans_kbrd(plans: list) -> json:
    """Список тематических планирований, на которые подписан юзер.
    Args:
        plans (dict): Список с информацией о тематических планах.
    Returns:
        json: Клавиатура в формате json.
    """
    pkbd = {}
    keyboard = []
    for plan in plans:
        callback_data = 'group'
        inline_button = [{
            'text': f"ГРУППА: {plan['group_name']}",
            'callback_data': callback_data
        }]
        keyboard.append(inline_button)
        for item in plan['plans']:
            callback_data = f"item:{item['name']}:{item['id']}:{plan['group_id']}"
            inline_button = [{
                'text': item['name'],
                'callback_data': callback_data
            }]
            keyboard.append(inline_button)

    pkbd['inline_keyboard'] = keyboard
    return json.dumps(pkbd)


def items_kbrd(local: LocalData, items: QuerySet, group_id: int) -> json:
    """Список тем в тематическом планировании.
    Args:
        items (_type_): Выборка о темах из базы данных.
        group_id (int): id группы.
    Returns:
        json: Клавиатура в формате json.
    """
    ikbd = {}
    keyboard = []
    for item in items:
        row = []
        if item.link:
            inline_button = {
                'text': item.name,
                'url': item.link
            }
        else:
            inline_button = {
                'text': item.name,
                'callback_data': f'no_data_item:{item.name}'
            }
        row.append(inline_button)
        if item.type == 'p' and item.link:
            status_work = local.get_status_work(item, group_id)
            inline_button = {
                'text': status_work,
                'callback_data': f"push:p:{item.id}:{group_id}"
            }
            row.append(inline_button)
        keyboard.append(row)
        row = ()
    ikbd['inline_keyboard'] = keyboard
    return json.dumps(ikbd)
