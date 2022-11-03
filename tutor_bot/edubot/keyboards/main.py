import json
from bots.models import BotAdmin
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
            {'text': 'План'},
            {'text': 'Сообщение учителю'},
        ]
    ]
    if BotAdmin.objects.filter(chat=chat_id):
        buttons_admin = [
            {'text': 'Администрировать'},
        ]
        if int(chat_id) == int(settings.BIG_BOSS_ID):
            bbbutton = {'text': 'Сообщение админам'}
        else:
            bbbutton = {'text': 'Техподдержка'}
        buttons_admin.append(bbbutton)
        keyboard.append(buttons_admin)
    mkbrd['keyboard'] = keyboard
    mkbrd['one_time_keyboard'] = True
    mkbrd['resize_keyboard'] = True
    return json.dumps(mkbrd)
