import json


def main_kbrd(chat_id: int, is_admin: bool) -> str:
    """Главная клавиатура бота.

    Args:
        chat_id (int): Telegram chat_id юзера.
    Returns:
        str: Клавиатура в формате json.
    """
    if is_admin:
        buttons_message = [
            {'text': 'Администрировать'},
        ]
    else:
        buttons_message = [
            {'text': 'Сообщение учителю'},
        ]
    keyboard = [
        [{'text': 'Рейтинг'}, {'text': 'Моя статистика'}],
        buttons_message
    ]
    mkbrd = {
        'keyboard': keyboard,
        'one_time_keyboard': True,
        'resize_keyboard': True,
    }
    return json.dumps(mkbrd)


def hide_kbrd() -> str:
    """Скрываем клавиатуру."""
    return json.dumps({'hide_keyboard': True})
