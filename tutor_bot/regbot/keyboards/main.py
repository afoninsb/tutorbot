import json
from django.conf import settings


def main_kbrd(chat_id: int) -> json:
    """Главная клавиатура бота.
    Args:
        chat_id (int): Telegram chat_id юзера.
    Returns:
        json: Клавиатура в формате json.
    """
    mkbrd = {}
    keyboard = [
        [
            {'text': 'Администрировать'},
        ]
    ]
    if int(chat_id) == int(settings.BIG_BOSS_ID):
        bbbutton = [{'text': 'Сообщение админам'}]
    else:
        bbbutton = [{'text': 'Техподдержка'}]
    keyboard.append(bbbutton)
    mkbrd['keyboard'] = keyboard
    mkbrd['one_time_keyboard'] = False
    mkbrd['resize_keyboard'] = True
    return json.dumps(mkbrd)


def hide_kbrd() -> json:
    """Скрываем клавиатуру"""
    return json.dumps({'hide_keyboard': True})
