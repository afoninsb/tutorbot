import json


def main_kbrd(chat_id: int, is_admin: bool) -> json:
    """Главная клавиатура бота.
    Args:
        chat_id (int): Telegram chat_id юзера.
    Returns:
        json: Клавиатура в формате json.
    """
    mkbrd = {}
    keyboard = [
        [
            {'text': 'Рейтинг'},
            {'text': 'Моя статистика'},
        ]
    ]
    if is_admin:
        buttons_message = [
            {'text': 'Администрировать'},
        ]
    else:
        buttons_message = [
            {'text': 'Сообщение учителю'},
        ]
    keyboard.append(buttons_message)
    mkbrd['keyboard'] = keyboard
    mkbrd['one_time_keyboard'] = True
    mkbrd['resize_keyboard'] = True
    return json.dumps(mkbrd)


def hide_kbrd() -> json:
    """Скрываем клавиатуру"""
    return json.dumps({'hide_keyboard': True})
