import json
from typing import Union

from django.conf import settings


def main_kbrd(chat_id: Union[int, str]) -> str:
    """Главная клавиатура бота.

    Args:
        chat_id (int): Telegram chat_id юзера.
    Returns:
        str: Клавиатура в формате json.
    """
    if int(chat_id) == int(settings.BIG_BOSS_ID):
        bbbutton = [{'text': 'Сообщение админам'}]
    else:
        bbbutton = [{'text': 'Техподдержка'}]
    keyboard = [[{'text': 'Администрировать'}], bbbutton]
    mkbrd = {
        'keyboard': keyboard,
        'one_time_keyboard': False,
        'resize_keyboard': True,
    }
    return json.dumps(mkbrd)


def hide_kbrd() -> str:
    """Скрываем клавиатуру"""
    return json.dumps({'hide_keyboard': True})
